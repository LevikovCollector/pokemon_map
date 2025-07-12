from django.db import models  # noqa F401

# your models here


class Pokemon(models.Model):
    """
    Model describing pokemon
    """
    title_ru = models.CharField(max_length=200, null=True, blank=True, verbose_name="Название покемона на русском")
    title_en = models.CharField(max_length=200, null=True, blank=True, verbose_name="Название покемона на английском")
    title_jp = models.CharField(max_length=200, null=True, blank=True, verbose_name="Название покемона на японском")
    description = models.TextField(max_length=1500, null=True, blank=True,  verbose_name="Описание покемона")
    pokemon_img = models.ImageField(upload_to="pokemon_img", null=True, blank=True,  verbose_name="Картика покемона")
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name="next_evolution", verbose_name="Предыдущая эволюция")

    def __repr__(self):
        return f"{self.title_ru}"

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    """
     Model describing pokemon on the map
     """
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время появления")
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время исчезновения")
    level = models.IntegerField(default=0, verbose_name="Уровень")
    health = models.IntegerField(default=100, verbose_name="Здоровье")
    strength = models.IntegerField(default=1, verbose_name="Сила")
    defence = models.IntegerField(default=1, verbose_name="Защита")
    stamina = models.IntegerField(default=0, verbose_name="Выносливость")

    def __str__(self):
        return f'{self.pokemon.title_ru}_{self.level}_{self.lat}_{self.lon}'
