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
from dz_simple_database_vikulin_m25_555.utils.console.db_console_colors import Color
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbCommandTableInfo(DbCommandBase):
    TOKEN_SCHEMA = ("table info <имя_таблицы>")
    PARAMS_SCHEMA = [
        DbCommandParam(
            "имя_таблицы",
            str,
            "Имя таблицы, схема которой будет выведена",
            True,
        )
    ]
    DESCRIPTION = (
        "Выводит схему столбцов таблицы БД в следующем наборе атрибутов: \n"
        f"{Color.OKCYAN}1){Color.ENDC} имя столбца {Color.OKCYAN}(name){Color.ENDC}\n"
        f"{Color.OKCYAN}2){Color.ENDC} тип данных столбца {Color.OKCYAN}(datatype){Color.ENDC}\n"
        f"{Color.OKCYAN}3){Color.ENDC} признак обязательности заполнения "
        f"{Color.OKCYAN}(is_mandatory){Color.ENDC}\n"
        f"{Color.OKCYAN}4){Color.ENDC} признак первичного ключа записи БД "
        f"{Color.OKCYAN}(is_primary){Color.ENDC}"
    )

    RULES = [
        "Таблица должна существовать в схеме БД"
    ]

    NAME = "table info"

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandTableInfo.TOKEN_SCHEMA,
            DbCommandTableInfo.PARAMS_SCHEMA,
            DbCommandTableInfo.DESCRIPTION,
            DbCommandTableInfo.RULES,
            DbCommandTableInfo.NAME
        )


    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:
        create table info <имя_таблицы>
        """
        normalized_tokens = [token.lower() for token in params]
        table_token = normalized_tokens[0]
        info_token = normalized_tokens[1]
        if table_token != "table" or info_token != "info":
            raise DbCommandException("Нарушение семантики команды: TABLE INFO ...")
        table_name = normalized_tokens[2]
        try:
            validate_string(table_name, "TABLE")
        except Exception:
            raise DbCommandException("Нарушение семантики команды: "
                                     "некорректно задано название целевой таблицы")
        self.register_param_value(table_name)

    def execute(self) -> List[List[str]]:
        table_name:str = self.get_param_value(0)
        table = self.metadata.get_table_schema(table_name)

        # регистрируем схему результата
        self.result_title = f"Схема таблицы '{table_name}'"
        self.register_result_schema_item("Имя колонки")
        self.register_result_schema_item("Тип данных")
        self.register_result_schema_item("Обязательная?")
        self.register_result_schema_item("Первичный ключ?")

        return [
            [
                column.name,
                column.datatype.name,
                str(column.is_mandatory),
                str(column.is_primary)
            ]
            for column in table.columns
        ]
