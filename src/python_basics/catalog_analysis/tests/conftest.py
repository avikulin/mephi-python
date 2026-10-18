import pytest
from _fixtures.general_film_collections import (
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


@pytest.fixture
def empty_film_collection():
    return empty


@pytest.fixture
def singleton_film_collection():
    return singleton


@pytest.fixture
def same_2_film_collection():
    return same_2


@pytest.fixture
def same_3_film_collection():
    return same_3


@pytest.fixture
def random_2_film_collection():
    return random_2


@pytest.fixture
def random_3_film_collection():
    return random_3


@pytest.fixture
def same_genre_film_collection():
    return same_genre


@pytest.fixture
def same_year_film_collection():
    return same_year


@pytest.fixture
def same_rating_film_collection():
    return same_rating


@pytest.fixture
def same_duration_film_collection():
    return same_duration


@pytest.fixture
def same_actors_film_collection():
    return same_actors