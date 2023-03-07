import folium
import json

from django.http import HttpResponseNotFound, HttpRequest
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime

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
    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        if localtime(pokemon_entity.appeared_at) <= localtime() <= localtime(pokemon_entity.disappeared_at):
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                pokemon_entity.pokemon.photo.path
            )

    pokemons_on_page = []
    for pokemon_entity in pokemon_entities:
        if localtime(pokemon_entity.appeared_at) <= localtime() <= localtime(pokemon_entity.disappeared_at):
            pokemons_on_page.append({
                'pokemon_id': pokemon_entity.pokemon.id,
                'img_url': pokemon_entity.pokemon.photo.path,
                'title_ru': pokemon_entity.pokemon.title,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_entities = PokemonEntity.objects.all()

    for pokemon_entity in pokemon_entities:
        if pokemon_entity.pokemon.id == int(pokemon_id):
            requested_pokemon_entity = pokemon_entity
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    add_pokemon(
        folium_map, requested_pokemon_entity.lat,
        requested_pokemon_entity.lon,
        requested_pokemon_entity.pokemon.photo.path
    )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': requested_pokemon_entity.pokemon, 'pokemon_id': requested_pokemon_entity.pokemon.id,
        'title_ru': requested_pokemon_entity.pokemon.title, 'img_url': requested_pokemon_entity.pokemon.photo.path
    })
