import re
import csv
import StringIO
import random
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from turker import models

def show(request):
    dictt = {}
    dictt.update(csrf(request))
    dictt['templates'] = []
    suitable_templates = models.Template.objects.filter(expect_suitable=True)
    for template in suitable_templates:
        template_part = {'name': template.name}
        memes = models.Meme.objects.filter(template=template).exclude(first_line_raw='')
        template_part['memes'] = []
        for meme in memes:
            reactions = models.Reaction.objects.filter(meme=meme)
            if not reactions.count():
                continue
            meme_part = {}
            meme_part['gag_id'] = meme.gag_id
            meme_part['normal_subject'] = template.normal_subject.title()
            meme_part['meme_subject'] = template.meme_subject.title()
            meme_part['first_line_you'] = meme.first_line_you.capitalize()
            if meme.second_line_you:
                meme_part['sure'] = True
                meme_part['second_line_you'] = meme.second_line_you.capitalize()
            else:
                meme_part['sure'] = False
                meme_part['second_line'] = meme.second_line_raw.capitalize()
            meme_part['reasonables'] = []
            for reaction in reactions:
                num_agrees = models.Agree.objects.filter(meme=meme).filter(reaction=reaction).count()
                reasonable = {
                    'text': reaction.text.capitalize(),
                    'num_agrees': num_agrees,
                }
                meme_part['reasonables'].append(reasonable)
            template_part['memes'].append(meme_part)
        if not template_part['memes']:
            continue
        dictt['templates'].append(template_part)
    return render_to_response('show_opposite.html', dictt)

def choose_reasonable(request):
    dictt = {}
    dictt.update(csrf(request))
    return render_to_response('choose_reasonable_opposite.html', dictt)

def upload_reasonable(request):
    if request.method != 'POST' or 'reasonable' not in request.FILES:
        return redirect('/opposite/')
    fr = request.FILES['reasonable']
    reader = csv.reader(fr)
    rows = [row for row in reader]
    rows.pop(0)
    for row in rows:
        meme_id = int(row[27])
        text = row[30]
        meme = models.Meme.objects.get(id=meme_id)
        try:
            models.Reaction.objects.filter(meme=meme).get(text=text)
            continue
        except models.Reaction.DoesNotExist:
            pass
        num_prev = models.Reaction.objects.filter(meme=meme).count()
        index = num_prev + 1
        reaction = models.Reaction(meme=meme, text=text, index=index, enabled=True)
        reaction.save()
    return redirect('/opposite/')

def choose_opposite(request):
    dictt = {}
    dictt.update(csrf(request))
    return render_to_response('choose_opposite_opposite.html', dictt)

def upload_opposite(request):
    if request.method != 'POST' or 'opposite' not in request.FILES:
        return redirect('/opposite/')
    fr = request.FILES['opposite']
    reader = csv.reader(fr)
    rows = [row for row in reader]
    rows.pop(0)
    conflicts = []
    for row in rows:
        meme_id = int(row[27])
        choice = row[35]
        text = row[36]
        turker_id = row[15]
        reactions_text = [row[31], row[32], row[33]]
        meme = models.Meme.objects.get(id=meme_id)
        same_turker_agrees = models.Agree.objects.filter(meme=meme).filter(turker_id=turker_id)
        if same_turker_agrees.count():
            assert same_turker_agrees.count() == 1
            same_turker_agree = same_turker_agrees[0]
            conflict_text = '{} answered {} on meme {} before'.format(turker_id, same_turker_agree.reaction.text, meme.gag_id)
            conflicts.append(conflict_text)
            continue
        elif choice != 'choice-other':
            assert not text.strip()
            mo = re.match('choice-(\d)', choice)
            assert mo
            choice_idx = int(mo.group(1)) - 1
            reaction = models.Reaction.objects.get(meme=meme, text=reactions_text[choice_idx])
        else:
            assert text.strip()
            try:
                reaction = models.Reaction.objects.get(meme=meme, text=text)
            except models.Reaction.DoesNotExist:
                pass
            old_enabled_reactions = models.Reaction.objects.filter(meme=meme).filter(enabled=True)
            disabled_reaction = random.choice(old_enabled_reactions)
            disabled_reaction.enabled = False
            disabled_reaction.save()
            num_prev = models.Reaction.objects.filter(meme=meme).count()
            index = num_prev + 1
            new_reaction = models.Reaction(meme=meme, text=text, index=index, enabled=True)
            new_reaction.save()
            reaction = new_reaction
        agree = models.Agree(meme=meme, reaction=reaction, turker_id=turker_id)
        agree.save()
    if conflicts:
        return render_to_response('conflict_opposite_opposite.html', {'conflicts': conflicts})
    return redirect('/opposite/')

def insert(request):
    if request.method != 'POST':
        return redirect('/opposite/')
    gag_id = request.POST.get('gag_id', None)
    second_line_you = request.POST.get('second_line_you', None)
    meme = models.Meme.objects.get(gag_id=gag_id)
    meme.second_line_you = second_line_you
    meme.save()
    return redirect('/opposite/#set-{}'.format(gag_id))

def dump(request):
    chooses = models.ChooseReasonable.objects.all()
    output = StringIO.StringIO()
    writer = csv.writer(output)
    writer.writerow(['meme_id', 'normal_subject', 'meme_subject', 'situation', 'reaction_1', 'reaction_2', 'reaction_3', 'punchline'])
    for choose in chooses:
        meme = choose.meme
        reactions = models.Reaction.objects.filter(meme=meme).filter(enabled=True).order_by('index')
        assert reactions.count() == 3
        completed = False
        for reaction in reactions:
            agrees = models.Agree.objects.filter(reaction=reaction)
            if agrees.count() >= 2:
                completed = True
                break
        if completed:
            continue
        row = [
            meme.id,
            meme.template.normal_subject.title(),
            meme.template.meme_subject.title(),
            meme.first_line_you.capitalize(),
            reactions[0].text,
            reactions[1].text,
            reactions[2].text,
            meme.second_line_you.capitalize(),
        ]
        writer.writerow(row)
    response = HttpResponse(output.getvalue(), mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=opposite-dump.csv'
    return response

