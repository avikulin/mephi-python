import pytest

from catalog_analysis.func.collections.list_utils import _get_movie_rating


def test_get_movie_rating_singleton(singleton_film_collection):
    assert _get_movie_rating(singleton_film_collection) == [
        ("The Dune Chronicles", 8.6)
    ]


def test_get_movie_rating_random_2(random_2_film_collection):
    assert _get_movie_rating(random_2_film_collection) == [
        ("Two Left Shoes", 6.0),
        ("Kitchen Stories", 5.9),
    ]


def test_get_movie_rating_random_3(random_3_film_collection):
    assert _get_movie_rating(random_3_film_collection) == [
        ("The Last Bakery", 9.2),
        ("The Quiet Algorithm", 9.2),
        ("The Dune Chronicles", 8.6),
    ]


def test_get_movie_rating_same_rating_stable_order(same_rating_film_collection):
    assert _get_movie_rating(same_rating_film_collection) == [
        ("The Last Bakery", 9.2),
        ("The Quiet Algorithm", 9.2),
    ]


def test_get_movie_rating_same_2(same_2_film_collection):
    expected = [("Kitchen Stories", 5.9)] * 2
    assert _get_movie_rating(same_2_film_collection) == expected


def test_get_movie_rating_same_3(same_3_film_collection):
    expected = [("The Last Bakery", 9.2)] * 3
    assert _get_movie_rating(same_3_film_collection) == expected


def test_get_movie_rating_empty(empty_film_collection):
    assert _get_movie_rating(empty_film_collection) == []


def test_get_movie_rating_none_raises():
    with pytest.raises(ValueError):
        _get_movie_rating(None)


def test_get_movie_rating_returns_list_of_tuples(random_2_film_collection):
    result = _get_movie_rating(random_2_film_collection)
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) for item in result)
