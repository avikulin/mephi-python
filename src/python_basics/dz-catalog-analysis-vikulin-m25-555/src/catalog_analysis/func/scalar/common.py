import math
from typing import Any, Dict, List, Literal, Tuple

from catalog_analysis.data_samples.metadata import DURATION_KEY, RATING_KEY, YEAR_KEY
from catalog_analysis.func.helpers import clear


def average_rating(movies: List[Dict[str, Any]]) -> float:
    """Возвращает среднюю оценку по каталогу, округленную до одного знака."""
    clear_movies = clear(movies)  # делаем очистку от вкраплений None

    movies_length: int = len(movies)
    clear_movies_length: int = len(clear_movies)

    if movies_length == 0 | clear_movies_length == 0:
        return 0

    if clear_movies_length == 1:
        return clear_movies[0][RATING_KEY]

    avg_rating = 0
    for movie in clear_movies:
        avg_rating += movie[RATING_KEY]

    # делим на количество фильмов в исходном (неочищенном) списке
    avg_rating /= movies_length

    return round(avg_rating, 1)


def catalog_age_stats(
    movies: List[Dict[str, Any]], current_year: int = 2026
) -> Tuple[int, int, int]:
    """Возвращает кортеж (самый старый фильм в годах, самый новый
    фильм в годах, среднее), где среднее округлено вверх до целого с
    помощью math.ceil."""
    earliest_year = current_year + 1
    latest_year = -1
    sum_years = 0
    movies_length = len(movies)

    for movie in clear(movies):
        year = movie[YEAR_KEY]
        earliest_year = min(earliest_year, year)
        latest_year = max(latest_year, year)
        sum_years += year

    return latest_year, earliest_year, math.ceil(sum_years / movies_length)


def duration_in_hours(minutes: int) -> str:
    """Возвращает строку в формате "2ч 35м"."""
    hours, remaining_minutes = divmod(minutes, 60)
    return f"{hours}ч {remaining_minutes}м"


def rating_tier(rating: int) -> Literal["шедевр", "хорошо", "средне", "слабо"]:
    """Возвращает категорию оценки."""
    tier = None

    if rating >= 9:
        tier = "шедевр"
    elif 7 <=rating < 9:
        tier = "хорошо"
    elif 5<= rating < 7:
        tier = "средне"

    return tier if rating >=5 else "слабо"


def decade_label(year: int) -> str:
    """Возвращает метку по году."""

    match year:
        case _ if year > 2020:
            return "новые"
        case _ if 2015 <= year <= 2020:
            return "недавние"
        case _ if year < 2015:
            return "старые"
    # предохранитель
    raise ValueError(f"Unexpected behaviour of function for value: <{year}>")


def count_long_movies(movies: List[Dict[str, Any]], threshold: int = 120) -> int:
    """Возвращает количество фильмов длиннее threshold минут."""
    count = 0
    for movie in clear(movies):
        if movie[DURATION_KEY] > threshold:
            count += 1
    return count
