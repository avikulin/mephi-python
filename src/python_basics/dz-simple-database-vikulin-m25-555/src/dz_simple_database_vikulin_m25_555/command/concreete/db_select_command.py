from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import DbCommandBase
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import DbCommandParam
from dz_simple_database_vikulin_m25_555.expression.db_predicate_factory import DbPredicateFactory
from dz_simple_database_vikulin_m25_555.expression.db_predicate import DbPredicate
from dz_simple_database_vikulin_m25_555.metadata_store.db_metadata_store import DbMetadataStore
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.table_store.db_table_store import DbTableStore
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbCommandSelect(DbCommandBase):
    token_schema = "select from <имя_таблицы> where <столбец> = <значение>"
    params_schema = [
        DbCommandParam("имя_таблицы", DbTable,
                       "Имя таблицы, в которой будет производиться отбор строк", True),
        DbCommandParam("[столбец]=[значение]", DbPredicate,
                       "Условие (предикат) отбора записей таблицы. ", False)
    ]
    description = ("Возращает набор записей указанной таблицы (<имя_таблицы>),\n "
                   "которые удовлетворяют переданному предикату: <столбец> = <значение>")

    rules = [
                   "Предикат может быть только один",
                   "Возвращаются все строки, соответствующие предикату",
                   "Возвращаются все атрибуты записи, указанные в схеме таблицы"
    ]
    def __init__(self, metadata:DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandSelect.token_schema,
            DbCommandSelect.params_schema,
            DbCommandSelect.description,
            DbCommandSelect.rules
        )
        self.table: DbTable = None
        self.table_store: DbTableStore = None
        self.predicate: DbPredicate = None

    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:
            select from <имя_таблицы> where <столбец> = <значение> или
            select from <имя_таблицы>"""
        #select = params[0]
        #from = params[1]
        table_name = params[2]
        validate_string(table_name,"TABLE")

        #WHERE = params[3]
        predicate = None
        if len(params) > 3:
            predicate = "".join(params[4:])

        self.table = super().metadata.get_table_schema(table_name)
        self.table_store = super().metadata.get_table_store(table_name)
        super().params_values.append(self.table)
        if predicate is not None:
            self.predicate = DbPredicateFactory.process_predicate(predicate,
                                                                  self.table)
            super().params_values.append(self.predicate)

    def execute(self) -> List[List[str]]:
        predicate = self._get_param_value(1)
        return self.table_store.select_tuples(predicate)


