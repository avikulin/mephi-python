from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import (
    DbCommandBase,
    DbCommandException,
)
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import (
    DbCommandParam,
)
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import (
    DbMetadataStore,
)
from dz_simple_database_vikulin_m25_555.persistence.table_store.db_table_store import (
    DbTableStore,
)
from dz_simple_database_vikulin_m25_555.utils.console.db_console_colors import Color
from dz_simple_database_vikulin_m25_555.utils.parsing.expr_parser import ParseExprHelper
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbCommandInsert(DbCommandBase):
    TOKEN_SCHEMA = "insert into <имя_таблицы> values (<значение1>, <значение2>, ...)"
    PARAMS_SCHEMA = [
        DbCommandParam(
            "имя_таблицы",
            DbTable,
            "Имя таблицы, в которую будет производиться вставка значений строки",
            True,
        ),
        DbCommandParam(
            "значение1..N",
            List[str],
            "Значения колонок, которые будут вставлены в строку",
            True,
        ),
    ]
    DESCRIPTION = (
        f"Выполняет вставку новой строки в таблицу ({Color.OKCYAN}<имя_таблицы>{Color.ENDC}),\n"
        "заполняя значения колонок слева направо в переданном порядке: \n"
        f"{Color.OKCYAN}<значение1>{Color.ENDC}, {Color.OKCYAN}<значение2>{Color.ENDC}, ...\n"
        "Вставленные строки возвращаются в качестве результата выполнения команды."
    )

    RULES = [
        "Порядок значений должен соответствовать порядку столбцов таблицы",
        "Типы значений должны соответствовать типа столбцов таблицы",
        "Значение ИД должно быть первым по счету",
        "Значение ИД должно быть целочисленным значением",
        "Значение ИД должно быть уникальным в рамках таблицы",
        "Возвращаются все строки, которые были вставлены в таблицу",
        "Возвращаются все колонки вставленных строк, указанные в схеме таблицы",
    ]

    NAME = "insert"

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandInsert.TOKEN_SCHEMA,
            DbCommandInsert.PARAMS_SCHEMA,
            DbCommandInsert.DESCRIPTION,
            DbCommandInsert.RULES,
            DbCommandInsert.NAME
        )
        self.table: DbTable = None
        self.table_store: DbTableStore = None

    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:
        select from <имя_таблицы> where <столбец> = <значение> или
        select from <имя_таблицы>"""
        insert_token = params[0].strip().lower()
        into_token = params[1].strip().lower()
        if insert_token != "insert" or into_token != "into":
            raise DbCommandException("Нарушение семантики команды: INSERT INTO ...")

        table_name = params[2].strip().lower()
        validate_string(table_name, "TABLE")

        self.table = self.metadata.get_table_schema(table_name)
        self.table_store = self.metadata.get_table_store(table_name)

        self.register_param_value(self.table)
        values_str = " ".join(params[3:])
        values = ParseExprHelper.parse_brackets(values_str,
                                                "VALUES (...)", ",")

        number_of_columns_wo_id = len(self.table.column_names) - 1 # считаем без ID
        number_of_values = len(values)
        if number_of_values != number_of_columns_wo_id:
            raise DbCommandException(
                f"Количество значений для вставки ({number_of_values}) "
                f"не соответствует количеству колонок ({number_of_columns_wo_id}) "
                f"таблицы '{table_name}'"
            )

        self.register_param_value(values)

    def execute(self) -> List[List[str]]:
        values: List[str] | None = self.get_param_value(1)
        if values is None:
            raise DbCommandException(
                f"Не зарегистрированы значения "
                f"для вставки во внутреннем контексте команды: "
                f"{self.number_of_values}"
            )

        # регистрируем схему результата
        self.result_title = f"В таблицу '{self.table.name}' добавлены строки"
        for column_name in self.table.column_names:
            self.register_result_schema_item(column_name)

        return self.table_store.insert_tuple(values)
