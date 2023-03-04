from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.title)
