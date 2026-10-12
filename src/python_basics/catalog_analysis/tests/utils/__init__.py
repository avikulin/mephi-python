from .fake_film_factory import create_film
from .general_film_collections import (
    empty,
    random_2,
    random_3,
    same_2,
    same_3,
    same_actors,
    same_duration,
    same_genre,
    same_rating,
    same_year,
    singleton,
)

__all__ = [
    "create_film",
    "empty",
    "singleton",
    "same_2",
    "same_3",
    "random_2",
    "random_3",
    "same_genre",
    "same_year",
    "same_rating",
    "same_duration",
    "same_actors"
]