from typing import Any, Dict, List

from catalog_analysis.data_samples import (
    TITLE_KEY,
    YEAR_KEY,
    GENRES_KEY,
    RATING_KEY,
    DURATION_KEY
)
from catalog_analysis.func.scalar.common import duration_in_hours

def normalize_title(title: str) -> str:
    """Приводит строку к формату Title Case (каждое слово с заглавной буквы)."""

    def capitalize(source):
        result = source[0].upper() + source[1:]
        return result

    if not title:
        return "" # предохранитель от None и пустой строки на вход
    return " ".join([capitalize(token.lower()) for token in title.split()])

def make_slug(title)->str:
    """Превращает нормализованное название 'The Quiet Algorithm' в «слаг» вида 'the-quiet-algorithm'"""
    if not title:
        return "" # предохранитель от None и пустой строки на вход
    result = title.strip().lower()

    # нормализуем подстроки с последовательными пробелами
    while "  " in result:
        result = result.replace("  ", " ") # тут хорошо бы regex, но написано, что можно только replace()

    return result.lower().replace(" ", "-")

def format_report_line(movie:Dict[str, Any]) -> str:
    """Возвращает единую строку с описанием фильма:
    'The Quiet Algorithm' (2024) - 9.2/10, 1ч 58м, жанры: drama, sci-fi
    Жанры сортируются лексикографически."""

    def sort_genres(g: List[str])-> List[str]:
        lowercase = [item.lower() for item in g]
        lowercase.sort() # экономим на аллокации списка
        return lowercase # учечки контекста не происходит - мы работаем с копией

    title = normalize_title(movie[TITLE_KEY])
    year = movie[YEAR_KEY]
    rating = f"{movie[RATING_KEY]}/10"
    duration = duration_in_hours(movie[DURATION_KEY])
    sorted_genres = sort_genres(movie[GENRES_KEY])
    genres = ', '.join(sorted_genres)

    return f"'{title}' ({year}) - {rating}, {duration}, жанры: {genres}"
