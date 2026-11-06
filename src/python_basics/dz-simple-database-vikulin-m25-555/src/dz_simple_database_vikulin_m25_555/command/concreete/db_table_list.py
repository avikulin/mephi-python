from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import DbCommandBase, DbCommandException
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import DbMetadataStore


class DbCommandTableList(DbCommandBase):
    TOKEN_SCHEMA = ("table list")
    PARAMS_SCHEMA = []
    DESCRIPTION = (
        "Выводит список таблиц, зарегистрированных в схеме БД."
    )

    RULES = [
        "Выводятся все существующие таблицы"
    ]

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandTableList.TOKEN_SCHEMA,
            DbCommandTableList.PARAMS_SCHEMA,
            DbCommandTableList.DESCRIPTION,
            DbCommandTableList.RULES,
        )


    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:
        create table info <имя_таблицы>
        """
        table_token = params[0].lower()
        list_token = params[1].lower()
        if table_token != "table" or list_token != "list":
            raise DbCommandException("Нарушение семантики команды: TABLE LIST")

    def execute(self) -> List[List[str]]:
        return [[table_name]
                for table_name in self.metadata.tables]