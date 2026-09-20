from catalog_analysis.data_samples import get_data, TITLE_KEY
from catalog_analysis.func.strings.string_utils import normalize_title, make_slug, format_report_line

if __name__ == "__main__":
    movies = get_data()


    print(f"Пример нормализации строки: {normalize_title(movies[0][TITLE_KEY])}")
    print(f"Пример slug-ификации строки: {make_slug(movies[0][TITLE_KEY])}")
    print(f"Пример составление отчета по фильму: {format_report_line(movies[0])}")