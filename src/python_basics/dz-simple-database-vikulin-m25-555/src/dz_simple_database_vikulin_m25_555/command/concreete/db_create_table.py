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
from dz_simple_database_vikulin_m25_555.utils.parsing.expr_parser import ParseExprHelper
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbCommandCreateTable(DbCommandBase):
    TOKEN_SCHEMA = ("create table <имя_таблицы> ( "
                    "<столбец1>:<тип1>, "
                    "<столбец2>:<тип2>, "
                    "... "
                    ")")
    PARAMS_SCHEMA = [
        DbCommandParam(
            "имя_таблицы",
            str,
            "Имя создаваемой таблицы",
            True,
        ),
        DbCommandParam(
            "[столбец]:[тип]",
            List[str],
            "Название и тип создаваемого столбца",
            True,
        ),
    ]
    DESCRIPTION = (
        f"Создает новую таблицу {Color.OKCYAN}<имя_таблицы>{Color.ENDC} "
        f"с указанным набором столбцов и их типами в схеме данных БД.\n"
        "Возвращает схему таблицы в качестве результата работы команды"
    )

    RULES = [
        "Имя таблицы должно быть уникально в рамках БД",
        "В названиях столбцов не допускаются пробелы"
        "Столбца должно быть уникально в рамках таблицы",
        f"Поддерживаются следующие типы данных: {Color.OKCYAN}STRING{Color.ENDC}, "
        f"{Color.OKCYAN}INTEGER{Color.ENDC}, {Color.OKCYAN}FLOAT{Color.ENDC}, "
        f"{Color.OKCYAN}DATETIME{Color.ENDC} и {Color.OKCYAN}BOOLEAN{Color.ENDC}",
    ]

    NAME = "create table"

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandCreateTable.TOKEN_SCHEMA,
            DbCommandCreateTable.PARAMS_SCHEMA,
            DbCommandCreateTable.DESCRIPTION,
            DbCommandCreateTable.RULES,
            DbCommandCreateTable.NAME
        )


    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:
        create table <имя_таблицы> (
            <столбец1>:<тип значение1>,
            <столбец2>:<тип значение2>,
            ...
        )
        """
        normalized_tokens = [token.lower() for token in params]
        create_token = normalized_tokens[0]
        table_token = normalized_tokens[1]
        if create_token != "create" or table_token != "table":
            raise DbCommandException("Нарушение семантики команды: CREATE TABLE ...")

        table_name = normalized_tokens[2]
        validate_string(table_name, "TABLE")
        self.register_param_value(table_name)

        columns_schema_str = "".join(normalized_tokens[3:])
        columns_schema_values = ParseExprHelper.parse_brackets(columns_schema_str,
           "<столбец1>:<тип значение1>, <столбец2>:<тип значение2>, ...", ",")
        self.register_param_value(columns_schema_values)


    def execute(self) -> List[List[str]]:
        table_name:str = self.get_param_value(0)
        column_schema_tokens:List[str] = self.get_param_value(1)
        schema = {}
        for column_schema in column_schema_tokens:
            if ":" not in column_schema:
                raise DbCommandException("Нарушение семантики "
                                         "<столбец>:<тип значение>. "
                                         "Не найден разделитель ':'")
            column_name, column_type = column_schema.split(":")
            schema[column_name] = column_type

        table = self.metadata.register_table(table_name, schema)

        # регистрируем схему результата
        self.result_title = f"Создана таблица '{table_name}'"
        self.register_result_schema_item("Имя колонки")
        self.register_result_schema_item("Тип данных")
        self.register_result_schema_item("Обязательная?")
        self.register_result_schema_item("Первичный ключ?")

        return [ [c.name, c.datatype, c.is_primary, c.is_mandatory]
                 for c in table.columns ]
