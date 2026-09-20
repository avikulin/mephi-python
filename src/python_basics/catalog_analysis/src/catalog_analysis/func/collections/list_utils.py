from typing import Dict, Any, Tuple, List

from catalog_analysis.data_samples import RATING_KEY, TITLE_KEY
from catalog_analysis.func.helpers import clear, protect_not_empty


def _get_movie_rating(movies: List[Dict[str, Any]])->List[Tuple[str, float]]:
    """Возвращает список кортежей "(название фильма, рейтинг)" в порядке убывания рейтинга"""
    sort_by_rating_desc =sorted(clear(movies), key=lambda f: f[RATING_KEY], reverse=True)
    return [(movie[TITLE_KEY], movie[RATING_KEY]) for movie in sort_by_rating_desc]


def titles_sorted_by_rating(movies: List[Dict[str, Any]]) -> List[str]:
    """Возвращает список названий фильмов, отсортированных по убыванию рейтинга"""
    protect_not_empty(movies)

    movie_title_idx = 0 # название фильма идет первым в кортеже
    return [movie_tuple[movie_title_idx] for movie_tuple in _get_movie_rating(movies)]

def top_n_by_rating(movies: List[Dict[str, Any]], n:int=3) -> List[Tuple[str, float]]:
    """Возвращает список из n кортежей (title, rating) — топ по рейтингу."""
    protect_not_empty(movies)

    if n > len(movies) or n < 0:
        raise ValueError("n-value must be over zero and must not exceed the size of entire list")

    return _get_movie_rating(movies)[0:n]