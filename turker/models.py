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

    # very dirty work
    def get_scene(self):
        if self.scene:
            return self.scene
        scene = self.first_line.lower()
        scene = 'you {}'.format(scene)
        return scene

class Log(models.Model):
    meme = models.ForeignKey(Meme)
    timestamp = models.DateTimeField(auto_now_add=True)

