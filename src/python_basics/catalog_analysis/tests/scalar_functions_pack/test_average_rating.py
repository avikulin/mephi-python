import pytest

from catalog_analysis.data_samples.metadata import RATING_KEY
from catalog_analysis.func.scalar.common import average_rating


def test_average_rating_none_collection():
    with pytest.raises(ValueError):
        average_rating(None)


def test_average_rating_empty_collection(empty_film_collection):
    assert(average_rating(empty_film_collection) == 0)


def test_average_rating_singleton(singleton_film_collection):
    item = singleton_film_collection[0]
    target_rating = item[RATING_KEY]
    assert(average_rating(singleton_film_collection) == target_rating)


def test_average_rating_same_2(same_2_film_collection):
    expected = same_2_film_collection[0][RATING_KEY]
    assert average_rating(same_2_film_collection) == expected


def test_average_rating_same_3(same_3_film_collection):
    expected = same_3_film_collection[0][RATING_KEY]
    assert average_rating(same_3_film_collection) == expected


def test_average_rating_same_rating(same_rating_film_collection):
    expected = same_rating_film_collection[0][RATING_KEY]
    assert average_rating(same_rating_film_collection) == expected


def test_average_rating_random_2(random_2_film_collection):
    ratings = [film[RATING_KEY] for film in random_2_film_collection]
    expected = round(sum(ratings) / len(ratings), 1)
    assert average_rating(random_2_film_collection) == expected


def test_average_rating_random_3(random_3_film_collection):
    ratings = [film[RATING_KEY] for film in random_3_film_collection]
    expected = round(sum(ratings) / len(ratings), 1)
    assert average_rating(random_3_film_collection) == expected