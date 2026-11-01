def run():
    """Основная точка входа:
    1. Загрузка актуальных метаданных с помощью load_metadata.
    2. Запрос строки ввода у пользователя.
    3. Разбор введенной строки на команду и аргументы."""


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")