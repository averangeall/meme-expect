from django.db import models

class Template(models.Model):
    name = models.TextField()
    normal_subject = models.TextField()
    meme_subject = models.TextField()
    expect_suitable = models.BooleanField()
    intro = models.TextField()

class Meme(models.Model):
    gag_id = models.TextField()
    template = models.ForeignKey(Template)
    first_line_raw = models.TextField()
    second_line_raw = models.TextField()
    expected_line = models.TextField()
    first_line_you = models.TextField()
    second_line_you = models.TextField()
    first_line_she = models.TextField()
    second_line_she = models.TextField()

class ChooseReasonable(models.Model):
    meme = models.ForeignKey(Meme)

class Reaction(models.Model):
    meme = models.ForeignKey(Meme)
    text = models.TextField()
    index = models.IntegerField()
    enabled = models.BooleanField()

class Agree(models.Model):
    meme = models.ForeignKey(Meme)
    reaction = models.ForeignKey(Reaction)
    turker_id = models.TextField()

class Log(models.Model):
    meme = models.ForeignKey(Meme)
    timestamp = models.DateTimeField(auto_now_add=True)

