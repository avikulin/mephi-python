from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import (
    DbCommandBase,
    DbCommandException,
)
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import (
    DbMetadataStore,
)


class DbCommandTableList(DbCommandBase):
    TOKEN_SCHEMA = ("table list")
    PARAMS_SCHEMA = []
    DESCRIPTION = (
        "Выводит список таблиц, зарегистрированных в схеме БД."
    )

    RULES = [
        "Выводятся все существующие таблицы"
    ]

    NAME = "table list"

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandTableList.TOKEN_SCHEMA,
            DbCommandTableList.PARAMS_SCHEMA,
            DbCommandTableList.DESCRIPTION,
            DbCommandTableList.RULES,
            DbCommandTableList.NAME
        )


    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:  table list """
        normalized_tokens = [token.lower() for token in params]
        table_token = normalized_tokens[0]
        list_token = normalized_tokens[1]
        if table_token != "table" or list_token != "list":
            raise DbCommandException("Нарушение семантики команды: TABLE LIST")

    def execute(self) -> List[List[str]]:
        # регистрируем схему результата
        self.result_title = "Список зарегистрированных таблиц БД"
        self.register_result_schema_item("Имя таблицы")
        tables = self.metadata.tables
        if len(tables) > 0:
            return [[table_name] for table_name in tables]
        else:
            return [["(пусто)"]]
