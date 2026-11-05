from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import DbCommandBase, DbCommandException
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import DbCommandParam
from dz_simple_database_vikulin_m25_555.command.expression.db_predicate import DbPredicate
from dz_simple_database_vikulin_m25_555.command.expression.factory.db_predicate_factory import DbPredicateFactory
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import DbMetadataStore
from dz_simple_database_vikulin_m25_555.persistence.table_store.db_table_store import DbTableStore
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbCommandDelete(DbCommandBase):
    TOKEN_SCHEMA = "delete from <имя_таблицы> where [столбец] = [значение]"
    PARAMS_SCHEMA = [
        DbCommandParam(
            "имя_таблицы",
            DbTable,
            "Имя таблицы, в которой будет производиться удаление строк",
            True,
        ),
        DbCommandParam(
            "[столбец]=[значение]",
            DbPredicate,
            "Условие (предикат) удаления записей таблицы ",
            False,
        ),
    ]
    DESCRIPTION = (
        "Выполняет удаление записей указанной таблицы (<имя_таблицы>),\n "
        "которые удовлетворяют переданному предикату: <столбец> = <значение>"
    )

    RULES = [
        "Предикат может быть только один",
        "Возвращаются все строки, которые были удалены",
        "Возвращаются все колонки удаленных строк, указанные в схеме таблицы",
    ]

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandDelete.TOKEN_SCHEMA,
            DbCommandDelete.PARAMS_SCHEMA,
            DbCommandDelete.DESCRIPTION,
            DbCommandDelete.RULES,
        )
        self.table: DbTable = None
        self.table_store: DbTableStore = None
        self.predicate: DbPredicate = None

    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:
        delete from <имя_таблицы> where <столбец> = <значение> или
        delete from <имя_таблицы>"""
        delete_token = params[0].lower()
        from_token = params[1].lower()
        if delete_token != "delete" or from_token != "from":
            raise DbCommandException("Нарушение семантики команды: "
                                     "DELETE FROM ...")
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
                raise DbCommandException("Нарушение семантики команды: "
                                         "WHERE ...")
            predicate = "".join(params[4:])

        self.table = self.metadata.get_table_schema(table_name)
        self.table_store = self.metadata.get_table_store(table_name)
        self.register_param_value(self.table)
        if predicate is not None:
            self.predicate = DbPredicateFactory.process_predicate(predicate, self.table)
            self.register_param_value(self.predicate)

    def execute(self) -> List[List[str]]:
        predicate = self.get_param_value(1)
        return self.table_store.delete_tuple(predicate)
