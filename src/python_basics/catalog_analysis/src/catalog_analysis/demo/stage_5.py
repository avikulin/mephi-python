from catalog_analysis.data_samples import TITLE_KEY, GENRES_KEY
from catalog_analysis.data_samples.movies import get_data
from catalog_analysis.func.collections.set_utils import all_genres, common_actors, genres_only_in_one
from catalog_analysis.func.helpers import clear

if __name__ == "__main__":
    movies = get_data()

    #--(1)--
    print("Перечень всех жанров:")
    print(all_genres(movies))

    #--(2)--
    movie1 = movies[0]
    movie2 = movies[3]
    print(f"\nПеречень общих актеров для фильмов \"{movie1[TITLE_KEY]}\" и \"{movie2[TITLE_KEY]}\":")
    print(common_actors(movie1, movie2))

    #--(3)--
    boundaries_a = (0, 3)
    boundaries_b = (3, 6)
    movies_a = movies[boundaries_a[0]:boundaries_a[1]]
    movies_b = movies[boundaries_b[0]:boundaries_b[1]]
    print(f"\nПеречень жанров первой выборки (с {boundaries_a[0]} по {boundaries_a[1]})")
    genres_a = set()
    for genres in  [movie[GENRES_KEY] for movie in clear(movies_a)]:
        genres_a.update(genres)

    for genre in genres_a:
        print(f"\t{genre}")

    print(f"\nПеречень жанров второй выборки (с {boundaries_b[0]} по {boundaries_b[1]})")
    genres_b = set()
    for genres in [movie[GENRES_KEY] for movie in clear(movies_b)]:
        genres_b.update(genres)

    for genre in genres_b:
        print(f"\t{genre}")

    print(f"\nПеречень общих жанров для подмножеств фильмов (с {boundaries_a[0]} по {boundaries_a[1]}) и "
                                                          f"(с {boundaries_b[0]} по {boundaries_b[1]}): "
                                                          f"{genres_only_in_one(movies_a, movies_b)}")
