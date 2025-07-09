from django.db import models  # noqa F401

# your models here


class Pokemon(models.Model):
    title = models.CharField(max_length=200)

    def __repr__(self):
        return f"{self.title}"

    def __str__(self):
        return f'{self.title}'
