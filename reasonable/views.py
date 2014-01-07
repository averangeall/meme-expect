from django.shortcuts import render_to_response
from turker import models

def show(request):
    dictt = {}
    dictt['templates'] = []
    suitable_templates = models.Template.objects.filter(expect_suitable=True)
    for template in suitable_templates:
        template_part = {'name': template.name}
        memes = models.Meme.objects.filter(template=template).exclude(first_line='')
        template_part['memes'] = []
        for meme in memes:
            meme_part = {}
            meme_part['gag_id'] = meme.gag_id
            meme_part['situation'] = 'You are a {subject}, and {scene}.'.format(subject=template.subject, scene=meme.get_scene())
            template_part['memes'].append(meme_part)
        dictt['templates'].append(template_part)
    return render_to_response('show_reasonable.html', dictt)

