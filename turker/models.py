from django.db import models

class Template(models.Model):
    name = models.TextField()

class Meme(models.Model):
    gag_id = models.TextField()
    template = models.ForeignKey(Template)
    first_line = models.TextField()
    second_line = models.TextField()
    expected_line = models.TextField()

