from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import (
    DbCommandBase,
    DbCommandException,
)
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import (
    DbCommandParam,
)
from dz_simple_database_vikulin_m25_555.command.expression.factory.db_predicate_factory import (
    DbPredicateFactory,
)
from dz_simple_database_vikulin_m25_555.command.expression.db_predicate import DbPredicate
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import (
    DbMetadataStore,
)
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.persistence.table_store.db_table_store import DbTableStore
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbCommandSelect(DbCommandBase):
    TOKEN_SCHEMA = "select from <имя_таблицы> where [столбец] = [значение]"
    PARAMS_SCHEMA = [
        DbCommandParam(
            "имя_таблицы",
            DbTable,
            "Имя таблицы, в которой будет производиться отбор строк",
            True,
        ),
        DbCommandParam(
            "[столбец]=[значение]",
            DbPredicate,
            "Условие (предикат) отбора записей таблицы. ",
            False,
        ),
    ]
    DESCRIPTION = (
        "Возвращает набор записей указанной таблицы (<имя_таблицы>),\n "
        "которые удовлетворяют переданному предикату: <столбец> = <значение>."
    )

    RULES = [
        "Предикат может быть только один",
        "Возвращаются все строки, соответствующие предикату",
        "Возвращаются все атрибуты записи, указанные в схеме таблицы",
    ]

    NAME = "select"

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandSelect.TOKEN_SCHEMA,
            DbCommandSelect.PARAMS_SCHEMA,
            DbCommandSelect.DESCRIPTION,
            DbCommandSelect.RULES,
            DbCommandSelect.NAME
        )
        self.table: DbTable = None
        self.table_store: DbTableStore = None
        self.predicate: DbPredicate = None

    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:
        select from <имя_таблицы> where <столбец> = <значение> или
        select from <имя_таблицы>"""
        select_token = params[0].lower()
        from_token = params[1].lower()
        if select_token != "select" or from_token != "from":
            raise DbCommandException("Нарушение семантики команды: SELECT FROM ...")
        table_name = params[2]
        try:
            validate_string(table_name, "TABLE")
        except Exception:
            raise DbCommandException("Нарушение семантики команды: "
                                     "некорректно задано название целевой таблицы")

        predicate = None
        if len(params) > 3:
            where_token = params[3].lower()
            if where_token != "where":
                raise DbCommandException("Нарушение семантики команды: WHERE ...")
            predicate = "".join(params[4:])

        self.table = self.metadata.get_table_schema(table_name)
        self.table_store = self.metadata.get_table_store(table_name)
        self.register_param_value(self.table)
        if predicate is not None:
            self.predicate = DbPredicateFactory.process_predicate(predicate, self.table)
            self.register_param_value(self.predicate)

    def execute(self) -> List[List[str]]:
        predicate = self.get_param_value(1)

        # регистрируем схему результата
        self.result_title = f"Из таблицы '{self.table.name}' получены строки"
        for column_name in self.table.column_names:
            self.register_result_schema_item(column_name)

        return self.table_store.select_tuples(predicate)
