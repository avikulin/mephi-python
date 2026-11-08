import pytest

from catalog_analysis.func.collections.dict_utils import actor_filmography


def test_actor_filmography_singleton(singleton_film_collection):
    assert actor_filmography(singleton_film_collection) == {
        "T. Chalamet": ["The Dune Chronicles"],
        "R. Ferguson": ["The Dune Chronicles"],
        "O. Isaac": ["The Dune Chronicles"],
    }


def test_actor_filmography_random_2(random_2_film_collection):
    assert actor_filmography(random_2_film_collection) == {
        "A. Novak": ["Two Left Shoes"],
        "K. Lee": ["Two Left Shoes"],
        "O. Isaac": ["Kitchen Stories"],
        "P. Diaz": ["Kitchen Stories"],
    }


def test_actor_filmography_random_3(random_3_film_collection):
    assert actor_filmography(random_3_film_collection) == {
        "A. Novak": ["The Last Bakery"],
        "T. Chalamet": ["The Last Bakery", "The Dune Chronicles"],
        "M. Ferguson": ["The Quiet Algorithm"],
        "O. Isaac": ["The Quiet Algorithm", "The Dune Chronicles"],
        "R. Ferguson": ["The Dune Chronicles"],
    }


def test_actor_filmography_same_actors(same_actors_film_collection):
    assert actor_filmography(same_actors_film_collection) == {
        "A. Novak": ["The Last Bakery", "Two Left Shoes"],
        "T. Chalamet": ["The Last Bakery"],
        "K. Lee": ["Two Left Shoes"],
    }


def test_actor_filmography_returns_dict_of_lists(random_2_film_collection):
    result = actor_filmography(random_2_film_collection)
    assert isinstance(result, dict)
    assert all(isinstance(films, list) for films in result.values())
    assert all(isinstance(title, str) for films in result.values() for title in films)


def test_actor_filmography_empty_raises(empty_film_collection):
    with pytest.raises(ValueError):
        actor_filmography(empty_film_collection)


def test_actor_filmography_none_raises():
    with pytest.raises(ValueError):
        actor_filmography(None)
