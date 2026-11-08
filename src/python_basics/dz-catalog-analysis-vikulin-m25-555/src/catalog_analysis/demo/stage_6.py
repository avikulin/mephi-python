from catalog_analysis.data_samples import RATING_KEY, TITLE_KEY
from catalog_analysis.data_samples.movies import get_data
from catalog_analysis.func.collections.dict_utils import (
    actor_filmography,
    count_by_genre,
)
from catalog_analysis.func.scalar import average_rating

if __name__ == "__main__":
    print("\nЭтап 6. Словари\n")
    movies = get_data()

    #--(1)--
    print("#1. Демонстрация функции `count_by_genre(movies)`")
    print("-------------------------------------------------")
    print("Выводим количество фильмов по каждому жанру:")
    print(count_by_genre(movies))
    print()

    # --(2)--
    print("#2. Демонстрация функции `actor_filmography(movies)`")
    print("----------------------------------------------------")
    print("\nВыводим фильмографию по каждому актеру:")
    print(actor_filmography(movies))
    print()

    #--(3)--
    print("#3. Демонстрация использования генератора словаря (dict comprehension)")
    print("----------------------------------------------------------------------")
    avg_rating = average_rating(movies)
    over_avg_rating = { movie[TITLE_KEY]:movie[RATING_KEY]
                        for movie in movies if movie[RATING_KEY] > avg_rating }

    print(f"\nСреднее значение рейтинга фильмов: {avg_rating}")
    print(f"Реализация словаря <title:rating> для фильмов, с рейтингом > {avg_rating}:")
    print(over_avg_rating)
    print()