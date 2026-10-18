import pytest

from catalog_analysis.func.collections.set_utils import all_genres


def test_all_genres_singleton(singleton_film_collection):
    assert all_genres(singleton_film_collection) == {"sci-fi"}


def test_all_genres_random_2(random_2_film_collection):
    assert all_genres(random_2_film_collection) == {"comedy", "sitcom"}


def test_all_genres_random_3(random_3_film_collection):
    assert all_genres(random_3_film_collection) == {"comedy", "sci-fi"}


def test_all_genres_same_genre(same_genre_film_collection):
    assert all_genres(same_genre_film_collection) == {"sci-fi"}


def test_all_genres_returns_set(random_3_film_collection):
    result = all_genres(random_3_film_collection)
    assert isinstance(result, set)
    assert all(isinstance(genre, str) for genre in result)


def test_all_genres_normalizes(random_3_film_collection):
    result = all_genres(random_3_film_collection)
    assert result == {genre.strip().lower() for genre in result}


def test_all_genres_empty_raises(empty_film_collection):
    with pytest.raises(ValueError):
        all_genres(empty_film_collection)


def test_all_genres_none_raises():
    with pytest.raises(ValueError):
        all_genres(None)
