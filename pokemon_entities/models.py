from django.db import models


class Pokemon(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    title = models.CharField('Название', max_length=200)
    photo = models.ImageField('Изображение', upload_to='photo', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    title_en = models.CharField('Название на английском', max_length=200, blank=True)
    title_jp = models.CharField('Название на японском', max_length=200, blank=True)
    next_evolution = models.ForeignKey('self', verbose_name='В кого эволюционирует', on_delete=models.SET_NULL,
                                       related_name='next_for', null=True, blank=True)
    previous_evolution = models.ForeignKey('self', verbose_name='Из кого эволюционирует', on_delete=models.SET_NULL,
                                           null=True, blank=True, related_name='previous_for')

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, related_name='entity', on_delete=models.CASCADE)
    lat = models.FloatField("Широта")
    lon = models.FloatField("Долгота")
    appeared_at = models.DateTimeField("Появление", null=True, blank=True)
    disappeared_at = models.DateTimeField("Исчезновение", null=True, blank=True)
    level = models.IntegerField("Уровень", null=True, blank=True)
    health = models.IntegerField("Здоровье", null=True, blank=True)
    strength = models.IntegerField("Сила", null=True, blank=True)
    defence = models.IntegerField("Защита", null=True, blank=True)
    stamina = models.IntegerField("Энергия", null=True, blank=True)

    def __str__(self):
        return 'pokemon entity'
