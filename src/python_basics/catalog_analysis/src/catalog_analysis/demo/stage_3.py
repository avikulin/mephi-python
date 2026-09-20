from catalog_analysis.func.collections.list_utils import titles_sorted_by_rating, top_n_by_rating
from catalog_analysis.data_samples.movies import get_data

if __name__ == "__main__":
    movies = get_data()

    #-- (1) --
    print("Вывод названий фильмов в порядке убывания рейтинга:")
    for title in titles_sorted_by_rating(movies):
        print(f"\t - {title};")

    #--(2)--
    print("\nВывод TOP-5 фильмов по рейтингу:")
    for title, rating in top_n_by_rating(movies, 5):
        print(f"\t - Название: \"{title}\", рейтинг: {rating}/10 ;")

    #--(3)--
    print(f"\nВывод рейтинга всех ({len(movies)} шт.) фильмов:")
    for title, rating in top_n_by_rating(movies, len(movies)):
        print(f"\t - Название: \"{title}\", рейтинг: {rating}/10 ;")
