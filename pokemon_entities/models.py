from django.db import models  # noqa F401

# your models here


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    pokemon_img = models.ImageField(upload_to="pokemon_img", null=True, blank=True)

    def __repr__(self):
        return f"{self.title}"

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)

