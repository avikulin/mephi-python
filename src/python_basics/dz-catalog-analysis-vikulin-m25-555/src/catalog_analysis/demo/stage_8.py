from catalog_analysis.data_samples import DURATION_KEY, RATING_KEY
from catalog_analysis.data_samples.movies import get_data
from catalog_analysis.func.generators.gen_utils import iter_high_rated
from catalog_analysis.func.strings.string_utils import format_report_line

if __name__ == "__main__":
    print("\nЭтап 8. Итераторы и генераторы\n")
    movies = get_data()
    MIN_RATING_THRESHOLD = 8
    print("#1. Демонстрация работы функции-генератора в цикле `for`")
    print("--------------------------------------------------------")

    print(f"Перечень фильмов с рейтингом ≥ {MIN_RATING_THRESHOLD}:\n")
    counter = 0
    for m in iter_high_rated(movies, MIN_RATING_THRESHOLD):
        print(f"\t- {format_report_line(m)}")
        counter += 1

    print(f"\n\tНайдено {counter} шт. из {len(movies)} шт.")
    print()

    print("#2. Демонстрация работы генераторного выражения")
    print("-----------------------------------------------")

    total_duration = sum(movie[DURATION_KEY]
                         for movie in movies
                         if movie[RATING_KEY] > 7)

    print(f"\tСуммарная длительность фильмов: {total_duration} мин.")
    print()