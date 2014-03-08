from django.core.context_processors import csrf
from django.shortcuts import render_to_response
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
            agree_cnts = {}
            for reaction in reactions:
                agrees = models.Agree.objects.filter(reaction=reaction)
                agree_cnts[reaction] = agrees.count()
            best_reaction = max(agree_cnts, key=agree_cnts.get)

            meme_part = {}
            meme_part['gag_id'] = meme.gag_id
            meme_part['first_move_sure'] = bool(template.intro)
            meme_part['first_move_line'] = template.intro if template.intro else ''
            meme_part['second_move_sure'] = bool(meme.first_line_she)
            meme_part['second_move_line'] = meme.first_line_she if meme.first_line_she else meme.first_line_raw.lower()
            meme_part['third_move_line'] = best_reaction.text.lower()
            meme_part['fourth_move_sure'] = bool(meme.second_line_she)
            meme_part['fourth_move_line'] = meme.second_line_she if meme.second_line_she else meme.second_line_raw.lower()
            template_part['memes'].append(meme_part)
        if not template_part['memes']:
            continue
        dictt['templates'].append(template_part)
    return render_to_response('show_explain.html', dictt)
