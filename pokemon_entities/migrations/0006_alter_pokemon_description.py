# Generated by Django 5.2.3 on 2025-07-10 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0005_remove_pokemon_title_pokemon_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='description',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]
