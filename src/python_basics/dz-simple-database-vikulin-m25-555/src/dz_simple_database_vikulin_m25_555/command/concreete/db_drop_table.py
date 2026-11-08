from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import (
    DbCommandBase,
    DbCommandException,
)
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import (
    DbCommandParam,
)
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import (
    DbMetadataStore,
)
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

    NAME = "drop table"

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandDropTable.TOKEN_SCHEMA,
            DbCommandDropTable.PARAMS_SCHEMA,
            DbCommandDropTable.DESCRIPTION,
            DbCommandDropTable.RULES,
            DbCommandDropTable.NAME
        )

    def parse_params(self, params: List[str]) -> None:
        """Ожидаем: drop table <имя_таблицы>"""
        normalized_tokens = [token.lower() for token in params]
        drop_token = normalized_tokens[0]
        table_token = normalized_tokens[1]
        if drop_token != "drop" or table_token != "table":
            raise DbCommandException("Нарушение семантики команды: DROP TABLE ...")
        table_name = normalized_tokens[2]
        validate_string(table_name, "TABLE")
        self.register_param_value(table_name)


    def execute(self) -> List[List[str]]:
        table_name:str = self.get_param_value(0)
        self.metadata.drop_table(table_name)
        # регистрируем схему результата
        self.result_title = "Удалена таблица"
        self.register_result_schema_item("Имя таблицы")
        return [ [table_name ] ]