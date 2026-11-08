
from dz_simple_database_vikulin_m25_555.command.concreete.db_create_table import (
    DbCommandCreateTable,
)
from dz_simple_database_vikulin_m25_555.command.concreete.db_delete_command import (
    DbCommandDelete,
)
from dz_simple_database_vikulin_m25_555.command.concreete.db_drop_table import (
    DbCommandDropTable,
)
from dz_simple_database_vikulin_m25_555.command.concreete.db_insert_command import (
    DbCommandInsert,
)
from dz_simple_database_vikulin_m25_555.command.concreete.db_select_command import (
    DbCommandSelect,
)
from dz_simple_database_vikulin_m25_555.command.concreete.db_table_info import (
    DbCommandTableInfo,
)
from dz_simple_database_vikulin_m25_555.command.concreete.db_table_list import (
    DbCommandTableList,
)
from dz_simple_database_vikulin_m25_555.command.concreete.db_update_command import (
    DbCommandUpdate,
)
from dz_simple_database_vikulin_m25_555.config.db_config import DbConfig
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import (
    DbMetadataStore,
)

if __name__ == "__main__":
    config = DbConfig()
    metadata = DbMetadataStore(config)

    exists = metadata.check_table_exists("books")
    print("Проверяем, существует ли таблица 'books': ", exists)

    if not exists:
        print("Таблицы такой нет. Создаем:")
        create_statement = ("create table books ("
                            "title : string, "
                            "author : string,  "
                            "year_of_publish : datetime, "
                            "pressrun_quantity : integer, "
                            "rating: float)")
        print(f"\t{create_statement}")
        create = DbCommandCreateTable(metadata)
        create.parse_string(create_statement)
        create.validate()
        print("Результат: ", create.execute())

    print("Выводим список таблиц:")
    ls = DbCommandTableList(metadata)
    ls.parse_string("table list")
    ls.validate()
    print(ls.execute())


    print("Выводим схему таблицы 'books'")
    info = DbCommandTableInfo(metadata)
    info.parse_string("table info books")
    info.validate()
    print(info.execute())

    select_1 = DbCommandSelect(metadata)
    select_1.parse_string("select from books where id = 1")
    select_1.validate()

    is_present = select_1.execute()
    print("Ищем существующую строку:")
    if len(is_present) > 0:
        print("Нашли: ", is_present)

    else:
        print("Не нашли. Вставляем новую...")
        insert = DbCommandInsert(metadata)
        insert.parse_string(
            "insert into books values "
            "(1, 'The Great Gatsby', 'F. Scott Fitzgerald', '1925-04-10T00:00:00', 300000, 4.7)"
        )
        insert.validate()
        result = insert.execute()
        print("Вставили новую строку: ", result)

        select_statement = "select from books where pressrun_quantity >= 300000"
        print("Теперь попробуем ее найти по условию: ")
        print(f"\t{select_statement}")
        select_2 = DbCommandSelect(metadata)
        select_2.parse_string(select_statement)
        select_2.validate()
        print("Результат: ",select_2.execute())

    print("Обновим значение рейтинга книги на 5.1")
    update = DbCommandUpdate(metadata)
    update.parse_string("update books set rating = 5.1 where id = 1")
    update.validate()
    result = update.execute()
    print("Обновленная строка: ", result)

    print("Найдем обновленную строку по значению:")
    select_statement_2 = "select from books where rating > 5"
    print(f"\t{select_statement_2}")

    select_3 = DbCommandSelect(metadata)
    select_3.parse_string(select_statement_2)
    select_3.validate()
    print("Результат: ", select_3.execute())

    print("Теперь попробуем удалить строку по условию:")
    delete_statement = "delete from books where year_of_publish = '1925-04-10T00:00:00'"
    print(f"\t{delete_statement}")
    delete = DbCommandDelete(metadata)
    delete.parse_string(delete_statement)
    delete.validate()
    result = delete.execute()
    print("Удаленный строки: ", result)

    print("Теперь посмотрим на строки, которые остались:")
    select_statement_4 = "select from books"
    print(f"\t{select_statement_4}")

    select_4 = DbCommandSelect(metadata)
    select_4.parse_string(select_statement_4)
    select_4.validate()
    print("Результат: ", select_4.execute())

    print("А теперь просто удалим таблицу 'books'")
    drop_statement = "drop table books"
    drop = DbCommandDropTable(metadata)
    drop.parse_string(drop_statement)
    drop.validate()
    print("Удалена таблица: ", drop.execute())