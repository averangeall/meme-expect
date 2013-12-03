import os
import re
import random
from django.shortcuts import render_to_response
from django.db.models import Count
import models

def expect(request):
    all_cnts = models.Meme.objects.filter(expected_line='').values('template').annotate(dcount=Count('template')).order_by('dcount')
    assert all_cnts.count()
    template_choice = random.randint(0, int(all_cnts.count() / 10.0) - 1)
    template = models.Template.objects.get(id=all_cnts[template_choice]['template'])
    print template.name
    memes = models.Meme.objects.filter(template=template)
    assert memes.count()
    print memes.count()
    meme_choice = random.randint(0, memes.count() - 1)
    print meme_choice
    meme = memes[meme_choice]
    return render_to_response('expect.html', {'meme': {'template': template.name, 'gag_id': meme.gag_id}})

def init(request):
    meme_root = 'turker/static/memes'
    templates = {}
    for dname in os.listdir(meme_root):
        cnt_old = 0
        cnt_new = 0
        try:
            template = models.Template.objects.get(name=dname)
        except models.Template.DoesNotExist:
            template = models.Template(name=dname)
            template.save()
        for fname in os.listdir(os.path.join(meme_root, dname)):
            mo = re.match(r'([^\.]+)\.jpg', fname)
            gag_id = mo.group(1)
            try:
                meme = models.Meme.objects.get(gag_id=gag_id)
                cnt_old += 1
            except models.Meme.DoesNotExist:
                meme = models.Meme(gag_id=gag_id, template=template)
                meme.save()
                cnt_new += 1
        templates[dname] = (cnt_old, cnt_new)
    return render_to_response('init.html', {'templates': templates})

