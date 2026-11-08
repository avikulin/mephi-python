import pytest

from catalog_analysis.func.collections import titles_sorted_by_rating


def test_titles_sorted_by_rating_singleton(singleton_film_collection):
    assert titles_sorted_by_rating(singleton_film_collection) == ["The Dune Chronicles"]


def test_titles_sorted_by_rating_random_2(random_2_film_collection):
    assert titles_sorted_by_rating(random_2_film_collection) == [
        "Two Left Shoes",
        "Kitchen Stories",
    ]


def test_titles_sorted_by_rating_random_3(random_3_film_collection):
    assert titles_sorted_by_rating(random_3_film_collection) == [
        "The Last Bakery",
        "The Quiet Algorithm",
        "The Dune Chronicles",
    ]


def test_titles_sorted_by_rating_same_rating_stable_order(same_rating_film_collection):
    assert titles_sorted_by_rating(same_rating_film_collection) == [
        "The Last Bakery",
        "The Quiet Algorithm",
    ]


def test_titles_sorted_by_rating_same_3(same_3_film_collection):
    expected = ["The Last Bakery"] * 3
    assert titles_sorted_by_rating(same_3_film_collection) == expected


def test_titles_sorted_by_rating_returns_strings(random_2_film_collection):
    result = titles_sorted_by_rating(random_2_film_collection)
    assert isinstance(result, list)
    assert all(isinstance(title, str) for title in result)


def test_titles_sorted_by_rating_empty_raises(empty_film_collection):
    with pytest.raises(ValueError):
        titles_sorted_by_rating(empty_film_collection)


def test_titles_sorted_by_rating_does_not_mutate_input(random_3_film_collection):
    original = [
        {
            key: (list(value) if isinstance(value, list) else value)
            for key, value in film.items()
        }
        for film in random_3_film_collection
    ]
    titles_sorted_by_rating(random_3_film_collection)
    assert random_3_film_collection == original


def test_titles_sorted_by_rating_none_raises():
    with pytest.raises(ValueError):
        titles_sorted_by_rating(None)
