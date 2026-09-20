import pytest

from catalog_analysis.func.collections.dict_utils import count_by_genre


def test_count_by_genre_singleton(singleton_film_collection):
    assert count_by_genre(singleton_film_collection) == {"sci-fi": 1}


def test_count_by_genre_random_2(random_2_film_collection):
    assert count_by_genre(random_2_film_collection) == {"comedy": 1, "sitcom": 1}


def test_count_by_genre_random_3(random_3_film_collection):
    assert count_by_genre(random_3_film_collection) == {"comedy": 1, "sci-fi": 2}


def test_count_by_genre_same_genre(same_genre_film_collection):
    assert count_by_genre(same_genre_film_collection) == {"sci-fi": 2}


def test_count_by_genre_returns_dict(random_2_film_collection):
    result = count_by_genre(random_2_film_collection)
    assert isinstance(result, dict)


def test_count_by_genre_empty_raises(empty_film_collection):
    with pytest.raises(ValueError):
        count_by_genre(empty_film_collection)


def test_count_by_genre_none_raises():
    with pytest.raises(ValueError):
        count_by_genre(None)
