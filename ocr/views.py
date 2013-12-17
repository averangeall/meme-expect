import random
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.db.models import Count
from turker import models

def write(request):
    dictt = {}
    dictt.update(csrf(request))
    templates = models.Meme.objects.filter(first_line='', second_line='').values('template').annotate()
    len(templates) # removing this line will cause templates.count() error (django bug?)
    assert templates.count()
    template_choice = random.randint(0, templates.count() - 1)
    template = models.Template.objects.get(id=templates[template_choice]['template'])
    memes = models.Meme.objects.filter(template=template)
    assert memes.count()
    meme_choice = random.randint(0, memes.count() - 1)
    meme = memes[meme_choice]
    assert meme.first_line == '' and meme.second_line == ''
    dictt['meme'] = {'template': template.name, 'gag_id': meme.gag_id}
    return render_to_response('write.html', dictt)

def insert(request):
    if request.method != 'POST':
        return redirect('/ocr/')
    gag_id = request.POST.get('gag_id')
    first_line = request.POST.get('line-1')
    second_line = request.POST.get('line-2')
    meme = models.Meme.objects.get(gag_id=gag_id)
    meme.first_line = first_line
    meme.second_line = second_line
    meme.save()
    log = models.Log(meme=meme)
    log.save()
    return redirect('/ocr/')
