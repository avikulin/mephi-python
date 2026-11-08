from catalog_analysis.data_samples import DURATION_KEY
from catalog_analysis.func.scalar import count_long_movies


def test_count_long_movies_empty(empty_film_collection):
    assert count_long_movies(empty_film_collection) == 0


def test_count_long_movies_singleton(singleton_film_collection):
    expected = int(singleton_film_collection[0][DURATION_KEY] > 120)
    assert count_long_movies(singleton_film_collection) == expected


def test_count_long_movies_same_duration(same_duration_film_collection):
    duration = same_duration_film_collection[0][DURATION_KEY]
    expected = len(same_duration_film_collection) if duration > 120 else 0
    assert count_long_movies(same_duration_film_collection) == expected


def test_count_long_movies_random_3(random_3_film_collection):
    expected = sum(film[DURATION_KEY] > 120 for film in random_3_film_collection)
    assert count_long_movies(random_3_film_collection) == expected


def test_count_long_movies_custom_threshold(singleton_film_collection):
    threshold = singleton_film_collection[0][DURATION_KEY] - 1
    assert count_long_movies(singleton_film_collection, threshold=threshold) == 1


def test_count_long_movies_threshold_lower_than_all(same_duration_film_collection):
    threshold = same_duration_film_collection[0][DURATION_KEY] + 1
    assert count_long_movies(same_duration_film_collection, threshold=threshold) == 0
