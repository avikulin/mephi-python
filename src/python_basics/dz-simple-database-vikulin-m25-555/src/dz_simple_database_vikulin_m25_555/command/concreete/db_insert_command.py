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
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.persistence.table_store.db_table_store import DbTableStore
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
            "<значение1..N>,",
            List[str],
            "Значения колонок, которые будут вставлены в строку",
            True,
        ),
    ]
    DESCRIPTION = (
        "Выполняет вставку новой строки в таблицу (<имя_таблицы>),\n "
        "заполняя значения колонок слева направо в переданном порядке: \n"
        "<значение1>, <значение2>, ..."
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

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandInsert.TOKEN_SCHEMA,
            DbCommandInsert.PARAMS_SCHEMA,
            DbCommandInsert.DESCRIPTION,
            DbCommandInsert.RULES,
        )
        self.table: DbTable = None
        self.table_store: DbTableStore = None

    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:
        select from <имя_таблицы> where <столбец> = <значение> или
        select from <имя_таблицы>"""

        insert_token = params[0].lower()
        into_token = params[1].lower()
        if insert_token != "insert" or into_token != "into":
            raise DbCommandException("Нарушение семантики команды: INSERT INTO ...")

        table_name = params[2].lower()
        try:
            validate_string(table_name, "TABLE")
        except Exception:
            raise DbCommandException("Нарушение семантики команды: "
                                     "некорректно задано название целевой таблицы")
        self.table = self.metadata.get_table_schema(table_name)
        self.table_store = self.metadata.get_table_store(table_name)

        self.register_param_value(self.table)
        values_token = params[3].lower()
        if values_token != "values":
            raise DbCommandException("Нарушение семантики команды: VALUES ...")

        values_str = "".join(params[4:])
        if ("(", ")") != (values_str[0], values_str[-1]):
            raise DbCommandException(
                f"Нарушена семантика передачи значений "
                f"на вставку в таблицу: "
                f"в выражении '{values_str}' не хватает скобок"
            )

        values = values_str[1:-1].split(",")
        number_of_columns = len(self.table.column_names)
        number_of_values = len(values)
        if number_of_values != number_of_columns:
            raise DbCommandException(
                f"Количество значений для вставки ({number_of_values}) "
                f"не соответствует количеству колонок ({number_of_columns}) "
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
