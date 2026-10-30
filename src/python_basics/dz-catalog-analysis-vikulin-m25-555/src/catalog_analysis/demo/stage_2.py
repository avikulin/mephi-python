from catalog_analysis.data_samples import TITLE_KEY, YEAR_KEY, GENRES_KEY, RATING_KEY
from catalog_analysis.data_samples.movies import get_data
from catalog_analysis.func.scalar.common import rating_tier, decade_label

if __name__ == "__main__":
    print("\nЭтап 2. Условия и `match`\n")

    movies = get_data()

    #(1)
    print("#1. Демонстрация функции `rating_tier(rating)`")
    print("----------------------------------------------")
    print("Категории оценок фильмов по рейтингу:")
    for idx, movie in enumerate(movies):
        name = movie[TITLE_KEY]
        year = movie[YEAR_KEY]
        genre = ", ".join(movie[GENRES_KEY])
        tier = rating_tier(movie[RATING_KEY])
        print(f"\t#{idx + 1}. {name}, {year} ({genre}) = [{tier}]")
    print()

    #(2)
    print("#2. Демонстрация функции `decade_label(year)`")
    print("----------------------------------------------")
    print("Категории оценок фильмов по времени выхода:")
    for idx, movie in enumerate(movies):
        name = movie[TITLE_KEY]
        year = movie[YEAR_KEY]
        genre = ", ".join(movie[GENRES_KEY])
        tier = decade_label(year)
        print(f"\t#{idx + 1}. {name}, {year} ({genre}) = [{tier}]")
    print()
