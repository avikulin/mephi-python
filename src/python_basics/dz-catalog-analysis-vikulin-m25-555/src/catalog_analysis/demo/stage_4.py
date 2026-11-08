from catalog_analysis.data_samples import TITLE_KEY, get_data
from catalog_analysis.func.strings.string_utils import (
    format_report_line,
    make_slug,
    normalize_title,
)

if __name__ == "__main__":
    print("\nЭтап 4. Строки\n")
    movies = get_data()

    # (1)
    print("#1. Демонстрация функции `normalize_title(title)`")
    print("-------------------------------------------------")
    print(f"Пример нормализации строки: {normalize_title(movies[0][TITLE_KEY])}")
    print()

    # (2)
    print("#2. Демонстрация функции `make_slug(title)`")
    print("-------------------------------------------")
    print(f"Пример slug-ификации строки: {make_slug(movies[0][TITLE_KEY])}")
    print()

    # (3)
    print("#3. Демонстрация функции `format_report_line(movie)`")
    print("----------------------------------------------------")
    print(f"Пример составление отчета по фильму: {format_report_line(movies[0])}")
    print()