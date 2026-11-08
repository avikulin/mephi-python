from catalog_analysis.func.strings import format_report_line


def test_format_report_line_singleton(singleton_film_collection):
    movie = singleton_film_collection[0]
    assert format_report_line(movie) == (
        "'The Dune Chronicles' (2021) - 8.6/10, 2ч 35м, жанры: sci-fi"
    )


def test_format_report_line_genres_sorted():
    movie = {
        "title": "the quiet algorithm",
        "year": 2024,
        "genres": ["sci-fi", "drama", "Action"],
        "rating": 9.2,
        "duration_min": 155,
    }
    assert format_report_line(movie) == (
        "'The Quiet Algorithm' (2024) - 9.2/10, 2ч 35м, жанры: action, drama, sci-fi"
    )


def test_format_report_line_single_genre():
    movie = {
        "title": "The Last Bakery",
        "year": 2014,
        "genres": ["comedy"],
        "rating": 9.2,
        "duration_min": 89,
    }
    assert format_report_line(movie) == (
        "'The Last Bakery' (2014) - 9.2/10, 1ч 29м, жанры: comedy"
    )


def test_format_report_line_does_not_mutate_genres(singleton_film_collection):
    movie = {
        **singleton_film_collection[0],
        "genres": ["sci-fi", "drama", "Action"],
    }
    original_genres = list(movie["genres"])
    format_report_line(movie)
    assert movie["genres"] == original_genres
