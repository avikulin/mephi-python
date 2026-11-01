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

    table_store.insert_tuple(["1", "The Great Gatsby", "F. Scott Fitzgerald", "1925-04-10T00:00:00", "300000", "4.7"])
    print(table_store.select_tuples(DbPredicate(table.columns[4],DbPredicateOperation.GE, 300000)))
