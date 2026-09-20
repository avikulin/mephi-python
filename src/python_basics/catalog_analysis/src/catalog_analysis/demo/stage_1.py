from typing import Dict, List, Any
from catalog_analysis.data_samples import get_data
from catalog_analysis.data_samples import (
    TITLE_KEY,
    YEAR_KEY,
    GENRES_KEY,
    RATING_KEY,
    DURATION_KEY,
    ACTORS_KEY
)
from catalog_analysis.func.scalar.common import duration_in_hours, count_long_movies

def film_pretty_print(film:Dict[str, Any]) -> None:
    print (f"\tНазвание: {film[TITLE_KEY]}\n"
           f"\tГод выпуска: {film[YEAR_KEY]}\n"
           f"\tЖанр: {', '.join(film[GENRES_KEY])}\n"
           f"\tРейтинг: {film[RATING_KEY]}\n"
           f"\tДлительность: {duration_in_hours(film[DURATION_KEY])}\n"
           f"\tАктерский состав: {', '.join(film[ACTORS_KEY])}")

def not_comedy(film:Dict[str, Any]) -> bool:
    filter_value = 'comedy'
    return not [genre for genre in film[GENRES_KEY] if genre.lower() == filter_value] # аналогично bool([]) == False

if __name__ == '__main__':
    # (1)
    print("\nA. Демонстрация фильтра по жанру (\"не комедия\" в цикле <for>:")
    films:List[Dict[str, Any]] = get_data()

    for num, item in enumerate(films):
        if not_comedy(item):
            print(f"\t{num}# Название: \"{item[TITLE_KEY]}\", жанры: \"{item[GENRES_KEY]}\"")

    # (2)
    print("\nB. Поиск первого по порядку фильма с рейтингом >9.0 с использованием while / break:")
    films_iter = iter(films)
    while True:
        try:
            item = next(films_iter)
            rating = item[RATING_KEY]
            if rating > 9:
                film_pretty_print(item)
                break # выходим на первом фильме с рейтингом > 9.0
        except StopIteration:
            break

    # (3)
    threshold_in_minutes = 100
    print(f"B. Подсчет кол-ва фильмов длиннее {threshold_in_minutes} мин. с помощью функции <count_long_movies>:")
    print(f"Результат: {count_long_movies(films, 100)}")
    print("Проверка:")

    item_idx = 0
    for item in films:
        if item[DURATION_KEY] > threshold_in_minutes:
            item_idx += 1
            print(f"\t---{item_idx}---")
            film_pretty_print(item)
            print()