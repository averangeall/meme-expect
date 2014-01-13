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
            meme_part = {}
            meme_part['gag_id'] = meme.gag_id
            meme_part['subject'] = template.subject
            try:
                models.ChooseReasonable.objects.get(meme=meme)
                meme_part['chosen'] = True
            except models.ChooseReasonable.DoesNotExist:
                meme_part['chosen'] = False
            if meme.scene:
                meme_part['sure'] = True
                meme_part['scene'] = meme.scene
            else:
                meme_part['sure'] = False
                meme_part['scene'] = meme.first_line.lower()
            template_part['memes'].append(meme_part)
        dictt['templates'].append(template_part)
    return render_to_response('show_reasonable.html', dictt)

def insert(request):
    if request.method != 'POST':
        return redirect('/reasonable/')
    gag_id = request.POST.get('gag_id')
    scene = request.POST.get('scene')
    meme = models.Meme.objects.get(gag_id=gag_id)
    meme.scene = scene
    meme.save()
    log = models.Log(meme=meme)
    log.save()
    return redirect('/reasonable/#set-{}'.format(gag_id))

def dump(request):
    memes = models.Meme.objects.exclude(scene='')
    output = StringIO.StringIO()
    writer = csv.writer(output)
    template_cnt = {}
    writer.writerow(['role', 'situation'])
    for meme in memes:
        writer.writerow([meme.template.subject, meme.scene])
    response = HttpResponse(output.getvalue(), mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=reasonable-dump.csv'
    return response

def choose(request, gag_id):
    meme = models.Meme.objects.get(gag_id=gag_id)
    try:
        models.ChooseReasonable.objects.get(meme=meme)
    except models.ChooseReasonable.DoesNotExist:
        choose = models.ChooseReasonable(meme=meme)
        choose.save()
    return redirect('/reasonable/#set-{}'.format(gag_id))

def remove(request, gag_id):
    meme = models.Meme.objects.get(gag_id=gag_id)
    try:
        choose = models.ChooseReasonable.objects.get(meme=meme)
        choose.delete()
    except models.ChooseReasonable.DoesNotExist:
        pass
    return redirect('/reasonable/#set-{}'.format(gag_id))

