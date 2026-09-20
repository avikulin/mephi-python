import pytest

from catalog_analysis.func.collections.list_utils import top_n_by_rating


def test_top_n_by_rating_default_n(random_3_film_collection):
    assert top_n_by_rating(random_3_film_collection) == [
        ("The Last Bakery", 9.2),
        ("The Quiet Algorithm", 9.2),
        ("The Dune Chronicles", 8.6),
    ]


def test_top_n_by_rating_n_2(random_3_film_collection):
    assert top_n_by_rating(random_3_film_collection, 2) == [
        ("The Last Bakery", 9.2),
        ("The Quiet Algorithm", 9.2),
    ]


def test_top_n_by_rating_n_1(random_3_film_collection):
    assert top_n_by_rating(random_3_film_collection, 1) == [("The Last Bakery", 9.2)]


def test_top_n_by_rating_n_0(random_3_film_collection):
    assert top_n_by_rating(random_3_film_collection, 0) == []


def test_top_n_by_rating_singleton(singleton_film_collection):
    assert top_n_by_rating(singleton_film_collection, 1) == [
        ("The Dune Chronicles", 8.6)
    ]


def test_top_n_by_rating_same_3(same_3_film_collection):
    expected = [("The Last Bakery", 9.2)] * 2
    assert top_n_by_rating(same_3_film_collection, 2) == expected


def test_top_n_by_rating_returns_tuples(random_2_film_collection):
    result = top_n_by_rating(random_2_film_collection, 2)
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) for item in result)


def test_top_n_by_rating_n_exceeds_length_raises(random_2_film_collection):
    with pytest.raises(ValueError):
        top_n_by_rating(random_2_film_collection, 3)


def test_top_n_by_rating_n_negative_raises(random_3_film_collection):
    with pytest.raises(ValueError):
        top_n_by_rating(random_3_film_collection, -1)


def test_top_n_by_rating_empty_raises(empty_film_collection):
    with pytest.raises(ValueError):
        top_n_by_rating(empty_film_collection)


def test_top_n_by_rating_none_raises():
    with pytest.raises(ValueError):
        top_n_by_rating(None)
