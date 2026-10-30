from typing import Any, Dict, List, Set

from catalog_analysis.data_samples import ACTORS_KEY, GENRES_KEY
from catalog_analysis.func.helpers import clear, protect_not_empty


def all_genres(films: List[Dict[str, Any]]) -> Set[str]:
    """Возвращает множество всех уникальных жанров каталога."""
    protect_not_empty(films)
    genres = set()
    for film in clear(films):
        # нормализация
        genres.update(genre.strip().lower() for genre in film[GENRES_KEY])
    return genres


def common_actors(movie1: Dict[str, Any], movie2: Dict[str, Any]) -> Set[str]:
    """Возвращает множество актеров, снимавшихся в обоих фильмах."""
    if not movie1:
        raise ValueError("Movie #1 must be not None")
    if not movie2:
        raise ValueError("Movie #2 must be not None")

    actors_1 = {actor.strip() for actor in movie1[ACTORS_KEY]}
    actors_2 = {actor.strip() for actor in movie2[ACTORS_KEY]}
    return actors_1 & actors_2

def genres_only_in_one(movies_a: List[Dict[str, Any]],
                       movies_b: List[Dict[str, Any]]) -> Set[str]:
    """Возвращает жанры, встречающиеся в <movies_a>,
    но не встречающиеся в <movies_b>"""

    protect_not_empty(movies_a)
    protect_not_empty(movies_b)

    genres_1 = set()
    for movie in clear(movies_a):
        # нормализация
        genres_1.update(genre.strip().lower() for genre in movie[GENRES_KEY])

    genres_2 = set()
    for movie in clear(movies_b):
        # нормализация
        genres_2.update(genre.strip().lower() for genre in movie[GENRES_KEY])

    return genres_1 - genres_2