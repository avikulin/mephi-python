from typing import List

from catalog_analysis.data_samples.metadata import (
    ACTORS_KEY,
    DURATION_KEY,
    GENRES_KEY,
    RATING_KEY,
    TITLE_KEY,
    YEAR_KEY,
)


def _construct_film(title: str,
                    year: int,
                    genres: List[str],
                    rating: float,
                    duration: int,
                    actors: List[str]):
    return {
        TITLE_KEY: title,
        YEAR_KEY: year,
        GENRES_KEY: genres,
        RATING_KEY: rating,
        DURATION_KEY: duration,
        ACTORS_KEY: actors
    }


def create_film(title: str,
                year: int,
                genre: str,
                rating: float,
                duration: int,
                actors: List[str]):
    return _construct_film(title, year, [genre], rating, duration, actors)