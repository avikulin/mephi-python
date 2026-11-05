from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import DbCommandBase, DbCommandException
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import DbCommandParam
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import DbMetadataStore
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbCommandDropTable(DbCommandBase):
    TOKEN_SCHEMA = ("drop table <имя_таблицы>")
    PARAMS_SCHEMA = [
        DbCommandParam(
            "имя_таблицы",
            str,
            "Имя таблицы, которая будет удалена",
            True,
        )
    ]
    DESCRIPTION = (
        "Удаляет указанную таблицу <имя_таблицы> из схемы данных БД. "
        "Возвращает имя удаленной таблицы."
    )

    RULES = [
        "Таблица должна существовать БД",
    ]

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandDropTable.TOKEN_SCHEMA,
            DbCommandDropTable.PARAMS_SCHEMA,
            DbCommandDropTable.DESCRIPTION,
            DbCommandDropTable.RULES,
        )

    def parse_params(self, params: List[str]) -> None:
        """Ожидаем: drop table <имя_таблицы>"""

        drop_token = params[0].lower()
        table_token = params[1].lower()
        if drop_token != "drop" or table_token != "table":
            raise DbCommandException("Нарушение семантики команды: DROP TABLE ...")
        table_name = params[2]
        try:
            validate_string(table_name, "TABLE")
        except Exception:
            raise DbCommandException("Нарушение семантики команды: "
                                     "некорректно задано название целевой таблицы")
        self.register_param_value(table_name)


    def execute(self) -> List[List[str]]:
        table_name = self.get_param_value(0)
        self.metadata.drop_table(table_name)
        return [ [table_name ] ]