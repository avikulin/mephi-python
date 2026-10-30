from typing import Any, Dict, List

from catalog_analysis.data_samples import RATING_KEY
from catalog_analysis.func.helpers import protect_not_empty


def iter_high_rated(movies:List[Dict[str, Any]], min_rating:float = 8.0):
    """"Лениво отдает (через yield) фильмы с рейтингом не ниже 'min_rating'"""

    protect_not_empty(movies)
    for movie in movies:
        if movie[RATING_KEY] > min_rating:
            yield movie
