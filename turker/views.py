import os
import re
from django.shortcuts import render_to_response
import models

def expect(request):
    return render_to_response('expect.html')

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

