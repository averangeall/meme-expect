import re
from django.shortcuts import render_to_response
from turker import models

def every(request):
    dictt = {}
    dictt['templates'] = []
    templates = models.Template.objects.all()
    for template in templates:
        item = {}
        item['name'] = template.name
        item['title'] = template.name.title()
        item['fname'] = re.sub(' ', '-', template.name) + '.jpg'
        dictt['templates'].append(item)
    return render_to_response('every.html', dictt)

def single(request, template_name):
    dictt = {}
    dictt['template'] = {'title': template_name.title(), 'name': template_name}
    template = models.Template.objects.get(name=template_name)
    memes = models.Meme.objects.filter(template=template)
    dictt['memes'] = [{'gag_id': meme.gag_id, 'first_line': meme.first_line_raw, 'second_line': meme.second_line_raw} for meme in memes]
    return render_to_response('single.html', dictt)
