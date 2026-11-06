from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import DbCommandBase, DbCommandException
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import DbCommandParam
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import DbMetadataStore
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
            "<столбец>:<тип>",
            List[str],
            "Название и тип создаваемого столбца",
            True,
        ),
    ]
    DESCRIPTION = (
        "Создает новую таблицу <имя_таблицы> с указанным набором столбцов и "
        "их типами в схеме данных БД. "
        "Возвращает схему таблицы в качестве результата работы команды"
    )

    RULES = [
        "Имя таблицы должно быть уникально в рамках БД",
        "В названиях столбцов не допускаются пробелы"
        "Столбца должно быть уникально в рамках таблицы",
        "Поддерживаются следующие типы данных: STRING, INTEGER, FLOAT, DATETIME и BOOLEAN",
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
        create_token = params[0].lower()
        table_token = params[1].lower()
        if create_token != "create" or table_token != "table":
            raise DbCommandException("Нарушение семантики команды: CREATE TABLE ...")
        table_name = params[2]
        try:
            validate_string(table_name, "TABLE")
        except Exception:
            raise DbCommandException("Нарушение семантики команды: "
                                     "некорректно задано название целевой таблицы")
        self.register_param_value(table_name)

        columns_schema_str = "".join(params[3:])
        if ("(", ")") != (columns_schema_str[0], columns_schema_str[-1]):
            raise DbCommandException(
                f"Нарушена семантика схемы колонок таблицы: "
                f"в выражении '{columns_schema_str}' не хватает скобок"
            )

        columns_schema_values = columns_schema_str[1:-1].split(",")
        self.register_param_value(columns_schema_values)


    def execute(self) -> List[List[str]]:
        table_name = self.get_param_value(0)
        column_schema_tokens = self.get_param_value(1)
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
