import types

import pytest

from catalog_analysis.func.generators.gen_utils import iter_high_rated


def test_iter_high_rated_singleton(singleton_film_collection):
    result = list(iter_high_rated(singleton_film_collection))
    assert [movie["title"] for movie in result] == ["The Dune Chronicles"]


def test_iter_high_rated_random_3_default(random_3_film_collection):
    result = list(iter_high_rated(random_3_film_collection))
    assert [movie["title"] for movie in result] == [
        "The Last Bakery",
        "The Quiet Algorithm",
        "The Dune Chronicles",
    ]


def test_iter_high_rated_random_2_default(random_2_film_collection):
    assert list(iter_high_rated(random_2_film_collection)) == []


def test_iter_high_rated_same_3(same_3_film_collection):
    result = list(iter_high_rated(same_3_film_collection))
    assert [movie["title"] for movie in result] == ["The Last Bakery"] * 3


def test_iter_high_rated_min_rating_9_2_excludes_equal(random_3_film_collection):
    assert list(iter_high_rated(random_3_film_collection, 9.2)) == []


def test_iter_high_rated_min_rating_5_0_includes_all(random_3_film_collection):
    result = list(iter_high_rated(random_3_film_collection, 5.0))
    assert [movie["title"] for movie in result] == [
        "The Last Bakery",
        "The Quiet Algorithm",
        "The Dune Chronicles",
    ]


def test_iter_high_rated_strictly_greater():
    movies = [{"title": "eq", "rating": 8.0}]
    assert list(iter_high_rated(movies)) == []


def test_iter_high_rated_returns_generator(random_3_film_collection):
    result = iter_high_rated(random_3_film_collection)
    assert isinstance(result, types.GeneratorType)


def test_iter_high_rated_lazy(random_3_film_collection):
    gen = iter_high_rated(random_3_film_collection)
    first = next(gen)
    assert first["title"] == "The Last Bakery"
    assert [movie["title"] for movie in gen] == [
        "The Quiet Algorithm",
        "The Dune Chronicles",
    ]


def test_iter_high_rated_does_not_mutate_input(random_3_film_collection):
    snapshot = [dict(movie) for movie in random_3_film_collection]
    list(iter_high_rated(random_3_film_collection))
    assert random_3_film_collection == snapshot


def test_iter_high_rated_empty_raises(empty_film_collection):
    with pytest.raises(ValueError):
        list(iter_high_rated(empty_film_collection))


def test_iter_high_rated_none_raises():
    with pytest.raises(ValueError):
        list(iter_high_rated(None))
