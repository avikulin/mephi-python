from typing import Any, Dict, List

from catalog_analysis.data_samples import ACTORS_KEY, GENRES_KEY, TITLE_KEY
from catalog_analysis.func.helpers import clear, protect_not_empty


def count_by_genre(movies: List[Dict[str, Any]]) -> Dict[str, int]:
    """Возвращает словарь {жанр: количество фильмов}"""
    protect_not_empty(movies)

    films_by_genre = {}
    for movie in clear(movies):
        genres = movie[GENRES_KEY]
        if not genres:
            raise ValueError("Genre must be not None or empty")

        for genre in genres:
            # если ничего не найдено - значит считаем с нуля
            genre = genre.strip().lower() # нормализуем
            current_counter_value = films_by_genre.get(genre, 0)
            current_counter_value += 1
            films_by_genre[genre] = current_counter_value

    return films_by_genre

def actor_filmography(movies: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Возвращает словарь {актер: [список названий фильмов]}"""
    protect_not_empty(movies)
    films_by_actor = {}

    for movie in clear(movies):
        actors = movie[ACTORS_KEY]
        if not actors:
            raise ValueError("Actor must be not None or empty")

        for actor in actors:
            actor = actor.strip() # нормализуем
            # если ничего не нашли - значит это первый фильм во вложенном списке
            current_actor_films = films_by_actor.get(actor, [])
            if len(current_actor_films) == 0:
                current_actor_films.append(movie[TITLE_KEY])
                films_by_actor[actor] = current_actor_films
            else:
                current_actor_films.append(movie[TITLE_KEY])

    return films_by_actor