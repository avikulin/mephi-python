import json

from dz_simple_database_vikulin_m25_555.config.db_config import DbConfig
from dz_simple_database_vikulin_m25_555.expression.db_predicate import DbPredicate
from dz_simple_database_vikulin_m25_555.expression.db_predicate_operation import DbPredicateOperation
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.table_store.db_table_store import DbTableStore

if __name__ == "__main__":
    table_schema = ""
    with open("sample_schema.json", "r") as file:
        table_schema = file.read()

    config = DbConfig()
    table = DbTable.from_json(table_schema)
    table_store = DbTableStore(table, config)

    id_filter = "ID = 1"
    id_predicate = table.process_predicate(id_filter)
    is_present = table_store.select_tuples(id_predicate)
    print("Ищем существующую строку:")
    print(is_present)
    print()
    if len(is_present) == 0:
        print("Не нашли. Вставляем новую...")
        table_store.insert_tuple(["1", "The Great Gatsby", "F. Scott Fitzgerald", "1925-04-10T00:00:00", "300000", "4.7"])
        predicate_str = "pressrun_quantity >= 300000"
        filter = table.process_predicate(predicate_str)
        print(table_store.select_tuples(filter))
        table_store.flush()

    #l, o, r = DbPredicateOperation.find_and_split(predicate_str)
    #print(table_store.select_tuples(DbPredicate(table.columns[4],DbPredicateOperation.GE, 300000)))
