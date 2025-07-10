import django
import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)





def show_all_pokemons(request):
    today = django.utils.timezone.localtime(django.utils.timezone.now())
    pokemons_entity = PokemonEntity.objects.filter(appeared_at__lte=today, disappeared_at__gte=today)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemons_entity:
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            request.build_absolute_uri(entity.pokemon.pokemon_img.url)
        )

    pokemons_on_page = []
    pokemon_already_exits = False
    for entity in pokemons_entity:
        for pokemon in pokemons_on_page:
            if entity.pokemon.id == pokemon['pokemon_id']:
                pokemon_already_exits = True

        if not pokemon_already_exits:
            pokemons_on_page.append({
                'pokemon_id': entity.pokemon.id,
                'img_url': request.build_absolute_uri(entity.pokemon.pokemon_img.url),
                'title_ru': entity.pokemon.title,
            })
        pokemon_already_exits = False

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']
    today = django.utils.timezone.localtime(django.utils.timezone.now())
    pokemons_entity = PokemonEntity.objects.filter(appeared_at__lte=today, disappeared_at__gte=today, id=pokemon_id)
    if not pokemons_entity:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemons_entity:
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            request.build_absolute_uri(entity.pokemon.pokemon_img.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_entity[0].pokemon
    })
