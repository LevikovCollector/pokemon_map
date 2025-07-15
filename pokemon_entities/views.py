import django
import folium

from django.shortcuts import render, get_object_or_404

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
                'title_ru': entity.pokemon.title_ru,
            })
        pokemon_already_exits = False

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    today = django.utils.timezone.localtime(django.utils.timezone.now())
    choosen_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemons_entity = PokemonEntity.objects.filter(appeared_at__lte=today, disappeared_at__gte=today)

    pokemon = {
        'pokemon_id': pokemon_id,
        'title_ru': choosen_pokemon.title_ru,
        'title_en': choosen_pokemon.title_en,
        'title_jp': choosen_pokemon.title_jp,
        'description': choosen_pokemon.description,
        'img_url': request.build_absolute_uri(choosen_pokemon.pokemon_img.url),
    }

    if choosen_pokemon.previous_evolution:
        pokemon["previous_evolution"] = {
            'title_ru': choosen_pokemon.previous_evolution.title_ru,
            'pokemon_id': choosen_pokemon.previous_evolution.id,
            'img_url': request.build_absolute_uri(choosen_pokemon.previous_evolution.pokemon_img.url)
        }
    next_evol = choosen_pokemon.next_evolutions.first()
    if next_evol:
        pokemon["next_evolution"] = {
            'title_ru': next_evol.title_ru,
            'pokemon_id': next_evol.id,
            'img_url': request.build_absolute_uri(next_evol.pokemon_img.url)
        }
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemons_entity:
        add_pokemon(
            folium_map, entity.lat,
            entity.lon,
            request.build_absolute_uri(entity.pokemon.pokemon_img.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
