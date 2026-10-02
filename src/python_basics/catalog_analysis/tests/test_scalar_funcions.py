import pytest
from data_samples import metadata


def test_average_rating_none_collection():
    with pytest.raises(ValueError) as ex:
        average_rating(None)

def test_average_rating_empty_collection(empty_film_collection):
    assert(average_rating(empty_film_collection) == 0)

def test_average_rating_singleton(singleton_film_collection):
    item = singleton_film_collection[0]
    target_rating = item[RATING_KEY]
    assert(average_rating(singleton_film_collection) == target_rating)

def test_average_rating_same_2():
    pass

def test_average_rating_same_3():
    pass

def test_average_rating_same_rating():
    pass

def test_average_rating_random_2():
    pass

def test_average_rating_random_3():
    pass

def test_average_rating_empty_collection(empty_film_collection):
    pass

def test_average_rating_singleton(singleton_film_collection):
    pass

def test_average_rating_same_2(same_2_film_collection):
    pass

def test_average_rating_same_3(same_3_film_collection):
    pass

def test_average_rating_same_rating(same_reating_film_collection):
    pass

def test_average_rating_random_2(random_2_film_collection):
    pass

def test_average_rating_random_3(random_3_film_collection):
    pass
