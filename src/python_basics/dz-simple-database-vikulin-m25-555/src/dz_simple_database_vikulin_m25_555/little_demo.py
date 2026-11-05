from pathlib import Path

from dz_simple_database_vikulin_m25_555.command.concreete.db_insert_command import (
    DbCommandInsert,
)
from dz_simple_database_vikulin_m25_555.command.concreete.db_select_command import (
    DbCommandSelect,
)
from dz_simple_database_vikulin_m25_555.command.concreete.db_update_command import DbCommandUpdate
from dz_simple_database_vikulin_m25_555.config.db_config import DbConfig
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import (
    DbMetadataStore,
)
from dz_simple_database_vikulin_m25_555.utils.io import read_json

if __name__ == "__main__":
    config = DbConfig()
    metadata = DbMetadataStore(config)

    table_schema = read_json(Path("books_schema.json"))
    metadata.register_table("books", table_schema)

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
