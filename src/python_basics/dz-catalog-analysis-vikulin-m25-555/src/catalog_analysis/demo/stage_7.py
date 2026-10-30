from catalog_analysis.data_samples import GENRES_KEY, TITLE_KEY
from catalog_analysis.data_samples.movies import get_data
from catalog_analysis.func.collections.set_utils import (
    all_genres,
    common_actors,
    genres_only_in_one,
)
from catalog_analysis.func.helpers import clear

if __name__ == "__main__":
    print("\nЭтап 7. Множества\n")
    movies = get_data()

    #--(1)--
    print("#1. Демонстрация функции `all_genres(movies)`")
    print("---------------------------------------------")
    print("Перечень всех жанров:")
    print(all_genres(movies))
    print()

    #--(2)--
    print("#2. Демонстрация функции `common_actors(movie1, movie2)`")
    print("--------------------------------------------------------")
    movie1 = movies[0]
    movie2 = movies[3]
    print(f"Перечень общих актеров для фильмов \"{movie1[TITLE_KEY]}\" и "
                                               f"\"{movie2[TITLE_KEY]}\":")
    print(common_actors(movie1, movie2))
    print()

    #--(3)--
    print("#3. Демонстрация функции `genres_only_in_one(movies_a, movies_b)`")
    print("-----------------------------------------------------------------")
    boundaries_a = (0, 3)
    boundaries_b = (3, 6)
    movies_a = movies[boundaries_a[0]:boundaries_a[1]]
    movies_b = movies[boundaries_b[0]:boundaries_b[1]]
    print(f"\n#3.Перечень жанров первой выборки (с {boundaries_a[0]} "
                                            f"по {boundaries_a[1]})")
    genres_a = set()
    for genres in  [movie[GENRES_KEY] for movie in clear(movies_a)]:
        genres_a.update(genres)

    for genre in genres_a:
        print(f"\t{genre}")

    print(f"\nПеречень жанров второй выборки (с {boundaries_b[0]} "
                                            f"по {boundaries_b[1]})")
    genres_b = set()
    for genres in [movie[GENRES_KEY] for movie in clear(movies_b)]:
        genres_b.update(genres)

    for genre in genres_b:
        print(f"\t{genre}")

    print(f"\nПеречень общих жанров для подмножеств фильмов "
          f"(с {boundaries_a[0]} по {boundaries_a[1]}) и "
          f"(с {boundaries_b[0]} по {boundaries_b[1]}): "
          f"{genres_only_in_one(movies_a, movies_b)}")
    print()