import csv
import StringIO
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
        memes = models.Meme.objects.filter(template=template).exclude(first_line='')
        template_part['memes'] = []
        for meme in memes:
            reactions = models.Reaction.objects.filter(meme=meme)
            if not reactions.count():
                continue
            meme_part = {}
            meme_part['gag_id'] = meme.gag_id
            meme_part['normal_subject'] = template.normal_subject.title()
            meme_part['meme_subject'] = template.meme_subject.title()
            meme_part['scene'] = meme.scene.capitalize()
            if meme.punchline:
                meme_part['sure'] = True
                meme_part['punchline'] = meme.punchline.capitalize()
            else:
                meme_part['sure'] = False
                meme_part['second_line'] = meme.second_line.capitalize()
            meme_part['reasonables'] = []
            for reaction in reactions:
                meme_part['reasonables'].append(reaction.text.capitalize())
            template_part['memes'].append(meme_part)
        if not template_part['memes']:
            continue
        dictt['templates'].append(template_part)
    return render_to_response('show_opposite.html', dictt)

def reasonable(request):
    dictt = {}
    dictt.update(csrf(request))
    return render_to_response('reasonable_opposite.html', dictt)

def upload(request):
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
        reaction = models.Reaction(meme=meme, text=text, index=index)
        reaction.save()
    return redirect('/opposite/')

def insert(request):
    if request.method != 'POST':
        return redirect('/opposite/')
    gag_id = request.POST.get('gag_id', None)
    punchline = request.POST.get('punchline', None)
    meme = models.Meme.objects.get(gag_id=gag_id)
    meme.punchline = punchline
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
        row = [
            meme.id,
            meme.template.normal_subject.title(),
            meme.template.meme_subject.title(),
            meme.scene.capitalize(),
            reactions[0].text,
            reactions[1].text,
            reactions[2].text,
            meme.punchline.capitalize(),
        ]
        writer.writerow(row)
    response = HttpResponse(output.getvalue(), mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=opposite-dump.csv'
    return response

