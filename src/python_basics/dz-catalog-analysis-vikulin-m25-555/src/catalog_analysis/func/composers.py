import math
from datetime import date
from typing import Any, Dict, List, Tuple

from catalog_analysis.data_samples import RATING_KEY, TITLE_KEY, YEAR_KEY
from catalog_analysis.func.collections import count_by_genre, top_n_by_rating
from catalog_analysis.func.collections.set_utils import all_genres
from catalog_analysis.func.helpers.helpers import clear, protect_not_empty
from catalog_analysis.func.strings import format_report_line


def get_avarage_rating_and_age(movies:List[Dict[str, Any]])->Tuple[float, int]:
    """Поскольку func_tools.reduce использовать нельзя - напишем свою реализацию.
    Будем делать все за один проход вширину (по исходной коллекции)
    + один reduce-проход вглубину"""
    current_year = date.today().year

    def project_tuple(movie_item: Dict[str, Any]) -> Tuple[float, int]:
        return movie_item[RATING_KEY], current_year - movie_item[YEAR_KEY]

    def sum_tuples(tuple1: Tuple[float, int], tuple2: Tuple[float, int]):
        return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]

    agg_values = (0.0, 0)
    for movie in movies:
        current = project_tuple(movie)
        agg_values = sum_tuples(agg_values, current)

    number_of_movies = len(movies)
    avg_rating = float(agg_values[0]) / number_of_movies
    avg_age = math.ceil(agg_values[1] / number_of_movies)
    return avg_rating, avg_age

def get_top_rated_movies(movies:List[Dict[str, Any]], threshold:int)->List[str]:
    """Формирование полных описаний подмножества из (threshold) фильмов
    с набольшим рейтингом"""
    movies_dict = {movie[TITLE_KEY]: movie for movie in movies}
    top_rated_names = (name_and_rating[0]
                       for name_and_rating in top_n_by_rating(movies, threshold))
    return [format_report_line(movies_dict[title]) for title in top_rated_names]

def get_genres_rating(movies:List[Dict[str, Any]])->List[Tuple[str, int]]:
    """Получение упорядоченного по убыванию количества фильмов списка жанров.
    Функция возвращает пары: (данр, количество фильмов по данному жанру)"""
    genres = list(all_genres(movies))
    number_by_genre: Dict[str, int] = count_by_genre(movies)
    sorted_genres = sorted(genres, key=lambda g: number_by_genre[g], reverse=True)
    return [(g, number_by_genre[g]) for g in sorted_genres]

def build_report(movies:List[Dict[str, Any]]):
    """Функция строит итоговый отчет со статистикой по каталогу фильмов"""
    protect_not_empty(movies)
    clear(movies)

    top_rated_movies = ["\t- " + movie
                        for movie in get_top_rated_movies(movies, 3)]

    avg_values = get_avarage_rating_and_age(movies)

    genres_rating = [f"\t{genre_stat[0]} - {genre_stat[1]}"
                     for genre_stat in get_genres_rating(movies)]

    genres_alphabetically = sorted(list(all_genres(movies)))

    templates = [
        "",
        "ОТЧЕТ ПО КАТАЛОГУ",
        "",
        f"Средний рейтинг: {avg_values[0]:.2f}",
        f"Средний возраст фильмов: {avg_values[1]} лет",
        "",
        "ТОП-3 фильма:",
        f"{"\n".join(top_rated_movies)}",
        "",
        "Фильмов по жанрам:",
        f"{"\n".join(genres_rating)}",
        "",
        f"Все жанры каталога: {", ".join(genres_alphabetically)}"
    ]

    return "\n".join(templates)
