from django.db import models

class Template(models.Model):
    name = models.TextField()
    subject = models.TextField()
    expect_suitable = models.BooleanField()

class Meme(models.Model):
    gag_id = models.TextField()
    template = models.ForeignKey(Template)
    first_line = models.TextField()
    second_line = models.TextField()
    expected_line = models.TextField()
    scene = models.TextField()

class Log(models.Model):
    meme = models.ForeignKey(Meme)
    timestamp = models.DateTimeField(auto_now_add=True)

