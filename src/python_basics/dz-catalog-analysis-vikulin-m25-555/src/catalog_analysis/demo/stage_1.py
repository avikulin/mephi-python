from catalog_analysis.data_samples import TITLE_KEY, YEAR_KEY, GENRES_KEY, DURATION_KEY
from catalog_analysis.data_samples.movies import get_data
from catalog_analysis.func.scalar.common import average_rating, catalog_age_stats, duration_in_hours

if __name__ == "__main__":
    print("\nЭтап 1. Разминка: переменные, числа, `math`\n")

    movies = get_data()

    #(1)
    print("#1. Демонстрация функции `average_rating(movies)`")
    print("-------------------------------------------------")
    print(f"\tСредняя оценка рейтинга по каталогу: {average_rating(movies)}")
    print()

    #(2)
    print("#2. Демонстрация функции `catalog_age_stats(movies, current_year=2026)`")
    print("-----------------------------------------------------------------------")
    age_stats = catalog_age_stats(movies)
    print(f"\tГод выхода самого старого фильма: {age_stats[0]}")
    print(f"\tГод выхода самого нового фильма: {age_stats[1]}")
    print(f"\tСреднее значение года выхода фильмов: {age_stats[2]}")
    print()

    #(3)
    print("#3. Демонстрация функции `duration_in_hours(minutes)`")
    print("-----------------------------------------------------")
    for idx, movie in enumerate(movies):
        name = movie[TITLE_KEY]
        year = movie[YEAR_KEY]
        duration = movie[DURATION_KEY]
        print(f"\t#{idx + 1}. {name}, {year} = {duration} мин. / {duration_in_hours(duration)}")

    print()
