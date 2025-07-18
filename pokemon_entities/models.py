from django.db import models  # noqa F401

# your models here


class Pokemon(models.Model):
    """
    Model describing pokemon
    """
    title_ru = models.CharField(max_length=200, verbose_name="Название покемона на русском")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Название покемона на английском")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="Название покемона на японском")
    description = models.TextField(max_length=1500, blank=True,  verbose_name="Описание покемона")
    pokemon_img = models.ImageField(upload_to="pokemon_img", verbose_name="Картика покемона")
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name="next_evolutions", verbose_name="Предыдущая эволюция")

    def __repr__(self):
        return f"{self.title_ru}"

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    """
     Model describing pokemon on the map
     """
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон",
                                related_name="entity")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(null=True, verbose_name="Дата и время появления")
    disappeared_at = models.DateTimeField(null=True, verbose_name="Дата и время исчезновения")
    level = models.IntegerField(default=1, verbose_name="Уровень", blank=True)
    health = models.IntegerField(default=100, verbose_name="Здоровье", blank=True)
    strength = models.IntegerField(default=1, verbose_name="Сила", blank=True)
    defence = models.IntegerField(default=1, verbose_name="Защита", blank=True)
    stamina = models.IntegerField(default=0, verbose_name="Выносливость", blank=True)

    def __str__(self):
        return f'{self.pokemon.title_ru}_{self.level}_{self.lat}_{self.lon}'
