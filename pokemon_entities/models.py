from django.db import models  # noqa F401

# your models here


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, null=True, blank=True)
    title_en = models.CharField(max_length=200, null=True, blank=True)
    title_jp = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=1500, null=True, blank=True)
    pokemon_img = models.ImageField(upload_to="pokemon_img", null=True, blank=True)

    def __repr__(self):
        return f"{self.title_ru}"

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=100)
    strength = models.IntegerField(default=1)
    defence = models.IntegerField(default=1)
    stamina = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pokemon.title_ru}_{self.level}_{self.lat}_{self.lon}'
