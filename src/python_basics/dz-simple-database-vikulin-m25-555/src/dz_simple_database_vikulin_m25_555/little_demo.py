from pathlib import Path

from dz_simple_database_vikulin_m25_555.command.concreete.db_insert_command import DbCommandInsert
from dz_simple_database_vikulin_m25_555.command.concreete.db_select_command import DbCommandSelect
from dz_simple_database_vikulin_m25_555.config.db_config import DbConfig
from dz_simple_database_vikulin_m25_555.metadata_store.db_metadata_store import DbMetadataStore
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.table_store.db_table_store import DbTableStore
from dz_simple_database_vikulin_m25_555.utils.io import read_json

if __name__ == "__main__":
    config = DbConfig()
    metadata = DbMetadataStore(config)

    table_schema = read_json(Path("sample_schema.json"))
    metadata.register_table("books", table_schema)

    select_1 = DbCommandSelect(metadata)
    select_1.parse_string("select from books where id = 1")
    select_1.validate()

    is_present = select_1.execute()
    print("Ищем существующую строку:")
    print(is_present)
    print()
    if len(is_present) == 0:
        print("Не нашли. Вставляем новую...")
        insert = DbCommandInsert(metadata)
        insert.parse_string("insert into books values "
                            "(1, 'The Great Gatsby', 'F. Scott Fitzgerald', '1925-04-10T00:00:00', 300000, 4.7)")
        insert.validate()
        insert.execute()
        print(insert.execute())

        select_2 = DbCommandSelect(metadata)
        select_2.parse_string("select from books where pressrun_quantity >= 300000")
        select_2.validate()
        print(select_2.execute())
        table_store.flush()
