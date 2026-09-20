import pytest

from catalog_analysis.func.collections.set_utils import common_actors


def test_common_actors_singleton_and_kitchen(
    singleton_film_collection, random_2_film_collection
):
    assert common_actors(singleton_film_collection[0], random_2_film_collection[1]) == {
        "O. Isaac"
    }


def test_common_actors_same_actors(same_actors_film_collection):
    assert common_actors(
        same_actors_film_collection[0], same_actors_film_collection[1]
    ) == {"A. Novak"}


def test_common_actors_no_intersection(
    same_genre_film_collection, random_2_film_collection
):
    assert (
        common_actors(same_genre_film_collection[0], random_2_film_collection[0])
        == set()
    )


def test_common_actors_returns_set(random_2_film_collection):
    result = common_actors(random_2_film_collection[0], random_2_film_collection[1])
    assert isinstance(result, set)
    assert all(isinstance(actor, str) for actor in result)


def test_common_actors_none_movie1_raises(random_2_film_collection):
    with pytest.raises(ValueError):
        common_actors(None, random_2_film_collection[0])


def test_common_actors_none_movie2_raises(random_2_film_collection):
    with pytest.raises(ValueError):
        common_actors(random_2_film_collection[0], None)


def test_common_actors_empty_dict_raises(random_2_film_collection):
    with pytest.raises(ValueError):
        common_actors({}, random_2_film_collection[0])
