from data_samples import metadata


def construct_film(title:str, 
                   year:int, 
                   genres:List[str], 
                   rating:float,
                   duration:int,
                   actors:List[str]):
    return {
        TITLE_KEY: title,
        YEAR_KEY: year,
        GENRES_KEY: genres,
        RATING_KEY: rating,
        DURATION_KEY: duration,
        ACTORS_KEY: actors
    }