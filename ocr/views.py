import random
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.db.models import Count
from turker import models

def write(request):
    dictt = {}
    dictt.update(csrf(request))

    templates = models.Template.objects.filter(expect_suitable=True)
    len_memes = models.Meme.objects.all().count()
    sorted_memes = [[] for i in range(len_memes)]
    for template in templates:
        empty_memes = models.Meme.objects.filter(template=template).filter(first_line_raw='').filter(second_line_raw='')
        fill_memes = models.Meme.objects.filter(template=template).exclude(first_line_raw='').exclude(second_line_raw='')
        sorted_memes[fill_memes.count()].extend(empty_memes)

    for memes in sorted_memes:
        if not memes:
            continue
        meme_choice = random.randint(0, len(memes) - 1)
        meme = memes[meme_choice]
        dictt['meme'] = {'template': meme.template.name, 'gag_id': meme.gag_id}
        break

    return render_to_response('write.html', dictt)

def insert(request):
    if request.method != 'POST':
        return redirect('/ocr/')
    gag_id = request.POST.get('gag_id')
    first_line_raw = request.POST.get('line-1')
    second_line_raw = request.POST.get('line-2')
    meme = models.Meme.objects.get(gag_id=gag_id)
    meme.first_line_raw = first_line_raw
    meme.second_line_raw = second_line_raw
    meme.save()
    log = models.Log(meme=meme)
    log.save()
    return redirect('/ocr/')
