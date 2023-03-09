import folium
from django.shortcuts import render, get_object_or_404
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
        icon=icon
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_time = localtime()
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=True, appeared_at__lt=current_time,
                                                       disappeared_at__gt=current_time):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.photo.path
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url,
            'title_ru': pokemon.title,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_time = localtime()
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=requested_pokemon, appeared_at__lt=current_time,
                                                       disappeared_at__gt=current_time):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            requested_pokemon.photo.path
        )
    pokemon_attributes = {'title_ru': requested_pokemon.title, 'img_url': requested_pokemon.photo.url,
                          'title_en': requested_pokemon.title_en, 'title_jp': requested_pokemon.title_jp,
                          'description': requested_pokemon.description,
                          'next_evolution': requested_pokemon.next_evolutions.first(),
                          'previous_evolution': requested_pokemon.previous_evolution}
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_attributes
    })
