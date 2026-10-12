import copy

from utils.fake_film_factory import create_film

films = [
    create_film(
        "The Dune Chronicles", 2021, "sci-fi", 8.6, 155,
        ["T. Chalamet", "R. Ferguson", "O. Isaac"],
    ),
    create_film("Kitchen Stories", 2019, "sitcom", 5.9, 101, ["O. Isaac", "P. Diaz"]),
    create_film(
        "The Last Bakery", 2014, "comedy", 9.2, 89,
        ["A. Novak", "T. Chalamet"],
    ),
    create_film("Two Left Shoes", 2019, "comedy", 6.0, 95, ["A. Novak", "K. Lee"]),
    create_film(
        "The Quiet Algorithm", 2024, "sci-fi", 9.2, 155,
        ["M. Ferguson", "O. Isaac"],
    ),
]

empty = []

singleton = [copy.deepcopy(films[0])]

same_2 = [copy.deepcopy(films[1]), copy.deepcopy(films[1])]

same_3 = [copy.deepcopy(films[2]), copy.deepcopy(films[2]), copy.deepcopy(films[2])]

random_2 = [copy.deepcopy(films[3]), copy.deepcopy(films[1])]

random_3 = [copy.deepcopy(films[2]), copy.deepcopy(films[4]), copy.deepcopy(films[0])]

same_genre = [copy.deepcopy(films[0]), copy.deepcopy(films[4])]

same_year = [copy.deepcopy(films[1]), copy.deepcopy(films[3])]

same_rating = [copy.deepcopy(films[2]), copy.deepcopy(films[4])]

same_duration = [copy.deepcopy(films[0]), copy.deepcopy(films[4])]

same_actors = [copy.deepcopy(films[2]), copy.deepcopy(films[3])]