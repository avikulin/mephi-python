import pytest

from catalog_analysis.func.collections import genres_only_in_one


def test_genres_only_in_one_random_3_minus_random_2(
    random_3_film_collection, random_2_film_collection
):
    assert genres_only_in_one(random_3_film_collection, random_2_film_collection) == {
        "sci-fi"
    }


def test_genres_only_in_one_random_2_minus_random_3(
    random_2_film_collection, random_3_film_collection
):
    assert genres_only_in_one(random_2_film_collection, random_3_film_collection) == {
        "sitcom"
    }


def test_genres_only_in_one_no_difference(
    singleton_film_collection, same_genre_film_collection
):
    assert (
        genres_only_in_one(singleton_film_collection, same_genre_film_collection)
        == set()
    )


def test_genres_only_in_one_returns_set(
    random_3_film_collection, random_2_film_collection
):
    result = genres_only_in_one(random_3_film_collection, random_2_film_collection)
    assert isinstance(result, set)
    assert all(isinstance(genre, str) for genre in result)


def test_genres_only_in_one_empty_a_raises(
    empty_film_collection, random_2_film_collection
):
    with pytest.raises(ValueError):
        genres_only_in_one(empty_film_collection, random_2_film_collection)


def test_genres_only_in_one_empty_b_raises(
    random_2_film_collection, empty_film_collection
):
    with pytest.raises(ValueError):
        genres_only_in_one(random_2_film_collection, empty_film_collection)


def test_genres_only_in_one_none_a_raises(random_2_film_collection):
    with pytest.raises(ValueError):
        genres_only_in_one(None, random_2_film_collection)


def test_genres_only_in_one_none_b_raises(random_2_film_collection):
    with pytest.raises(ValueError):
        genres_only_in_one(random_2_film_collection, None)
