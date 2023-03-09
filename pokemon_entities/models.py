from django.db import models


class Pokemon(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(verbose_name='Название', max_length=200)
    photo = models.ImageField(upload_to='photo', null=True, blank=True)
    description = models.TextField('Описание', null=True, blank=True)
    title_en = models.CharField(verbose_name='Название на английском', max_length=200, null=True, blank=True)
    title_jp = models.CharField(verbose_name='Название на японском', max_length=200, null=True, blank=True)
    next_evolution = models.ForeignKey('self', verbose_name='В кого эволюционирует', on_delete=models.SET_NULL, related_name='next_for', null=True, blank=True)
    previous_evolution = models.ForeignKey('self', verbose_name='Из кого эволюционирует', on_delete=models.SET_NULL, null=True,
                                       blank=True, related_name='previous_for')


    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name='entity', on_delete=models.CASCADE)
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return 'pokemon entity'