from typing import List, Dict

# 1) Функция average_rating(movies)
# ------------------------------------
# возвращает среднюю оценку по каталогу, округленную до одного знака (round).


# 2) Функция catalog_age_stats(movies, current_year=2026)
# ----------------------------------------------------
# возвращает кортеж (самый старый фильм в годах, самый новый фильм в годах, среднее), где среднее округлено вверх до целого с помощью math.ceil.

# *** Результат catalog_age_stats — неизменяемая запись, то есть tuple, а не список.


# 3) Функция duration_in_hours(minutes)
# ----------------------------------
# переводит минуты в формат "2ч 35м", используя целочисленное деление и остаток от деления.


# 4) Функция rating_tier(rating)
# ----------------------------
# по оценке возвращает категорию: "шедевр" (≥9), "хорошо" (7–8.9), "средне" (5–6.9), "слабо" (<5). Реализуйте ее через if/elif, а внутри используйте тернарный оператор хотя бы один раз.

# **** rating_tier обязательно содержит хотя бы один тернарный оператор.

# 5) Функция decade_label(year)
# -----------------------------
# которая через оператор match возвращает метку "новые" (после 2020), "недавние" (2015–2020) или "старые" (раньше 2015).

# *** decade_label обязательно реализована через match с использованием case _ if ... для сопоставления диапазонов.
# Границы диапазонов не должны пересекаться и не должны терять пограничные значения.


# 6) Функция count_long_movies(movies, threshold=120)
# -----------------------------------------------------
# которая через for с накопительной переменной считает количество фильмов длиннее threshold минут.

def average_rating(movies: List[Dict[str, Any]])->float:
    """Возвращает среднюю оценку по каталогу, округленную до одного знака."""
    RATING_KEY:str = 'rating'   # да, приходится дублировать код, чтобы не допускать жесткой связи между модулями
    movies_length:int = len(movies)

    if movies_length == 0:
        return 0
    if movies_length == 1:
        return movies[0][RATING_KEY]
    
    avg_rating = 0
    for movie in movies:
        avg_rating += movie[RATING_KEY]
    avg_rating /= movies_length

    return round(avg_rating, 1)


def catalog_age_stats(movies:List[Dict[str, Any]], current_year:int=2026) -> int:
    """Возвращает кортеж (самый старый фильм в годах, самый новый фильм в годах, среднее), где среднее округлено вверх до целого с помощью math.ceil."""
    YEAR_KEY:str = 'year'
    earliest_year = current_year + 1
    latest_year = -1

    for movie in movies:
        year = movie[YEAR_KEY]
        earliest_year = min(earliest_year, year)
        latest_year = max(latest_year, year)
    
    return (latest_year, earliest_year, math.ceil(average_rating(movies)))


def duration_in_hours(minutes:int):
    """Возвращает строку в формате "2ч 35м"."""
    pass

def rating_tier(rating: int):
    """Возвращает категорию оценки."""
    pass


def decade_label(year: int):
    """Возвращает метку по году."""
    pass


def count_long_movies(movies:Dict[str, Any], threshold:int=120):
    """Возвращает количество фильмов длиннее threshold минут."""
    pass
