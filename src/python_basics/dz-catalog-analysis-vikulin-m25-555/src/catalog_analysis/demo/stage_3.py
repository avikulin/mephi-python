from typing import Any, Dict, List

from catalog_analysis.data_samples import (
    ACTORS_KEY,
    DURATION_KEY,
    GENRES_KEY,
    RATING_KEY,
    TITLE_KEY,
    YEAR_KEY,
    get_data,
)
from catalog_analysis.func.scalar.common import count_long_movies, duration_in_hours


def film_pretty_print(film:Dict[str, Any]) -> None:
    print (f"\tНазвание: {film[TITLE_KEY]}\n"
           f"\tГод выпуска: {film[YEAR_KEY]}\n"
           f"\tЖанр: {', '.join(film[GENRES_KEY])}\n"
           f"\tРейтинг: {film[RATING_KEY]}\n"
           f"\tДлительность: {duration_in_hours(film[DURATION_KEY])}\n"
           f"\tАктерский состав: {', '.join(film[ACTORS_KEY])}")

def contains_comedy_genre(film:Dict[str, Any]) -> bool:
    filter_value = 'comedy'
    has_comedy = [genre for genre in film[GENRES_KEY] if genre.lower() == filter_value]
    return len(has_comedy) > 0

if __name__ == '__main__':
    print("\nЭтап 3. Циклы\n")

    # (1)
    print("#1. Демонстрация использования `for` и `continue`")
    print("-------------------------------------------------")
    print("Демонстрация фильтра по жанру (\"не комедия\" в цикле <for>:")
    films:List[Dict[str, Any]] = get_data()

    for num, item in enumerate(films):
        if contains_comedy_genre(item):
            continue
        print(f"\t{num}# Название: \"{item[TITLE_KEY]}\", "
                          f"жанры: \"{item[GENRES_KEY]}\"")
    print()

    # (2)
    print("#2. Демонстрация использования `while` и `break`")
    print("------------------------------------------------")
    print("Поиск первого по порядку фильма с рейтингом >9.0 "
               "с использованием while / break:")
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
    print()

    # (3)
    print("#3. Демонстрация функции `count_long_movies(movies, threshold=120)`")
    print("-------------------------------------------------------------------")
    threshold_in_minutes = 100
    print(f"Подсчет кол-ва фильмов длиннее {threshold_in_minutes} мин. "
          f"с помощью функции <count_long_movies>:")
    print(f"Результат: {count_long_movies(films, 100)}")
    print("\nПроверка:")

    item_idx = 0
    for item in films:
        if item[DURATION_KEY] > threshold_in_minutes:
            item_idx += 1
            print(f"\t---{item_idx}---")
            film_pretty_print(item)
            print()