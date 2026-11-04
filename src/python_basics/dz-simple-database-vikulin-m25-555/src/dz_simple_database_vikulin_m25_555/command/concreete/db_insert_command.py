from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import DbCommandBase, DbCommandException
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import DbCommandParam
from dz_simple_database_vikulin_m25_555.command.concreete.db_select_command import DbCommandSelect
from dz_simple_database_vikulin_m25_555.metadata_store.db_metadata_store import DbMetadataStore
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.table_store.db_table_store import DbTableStore
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbCommandInsert(DbCommandBase):
    token_schema = "insert into <имя_таблицы> values (<значение1>, <значение2>, ...)"
    params_schema = [
        DbCommandParam("имя_таблицы", DbTable,
                       "Имя таблицы, в которую будет производиться вставка значений строки", True),
        DbCommandParam("<значение1..N>,", List[str],
                       "Значения колонок, которые будут вставлены в строку", False)
    ]
    description = ("Выполняет вставку новой строки в таблицу (<имя_таблицы>),\n "
                   "заполняя значения колонок слева направо в переданном порядке: \n"
                   "<значение1>, <значение2>, ...")

    rules = [
        "Порядок значений должен соответствовать порядку столбцов таблицы",
        "Типы значений должны соответствовать типа столбцов таблицы",
        "Значение ИД должно быть первым по счету",
        "Значение ИД должно быть целочисленным значением",
        "Значение ИД должно быть уникальным в рамках таблицы"
    ]

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandSelect.token_schema,
            DbCommandSelect.params_schema,
            DbCommandSelect.description,
            DbCommandSelect.rules
        )
        self.table: DbTable = None
        self.table_store: DbTableStore = None

    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:
            select from <имя_таблицы> where <столбец> = <значение> или
            select from <имя_таблицы>"""
        # INSERT = params[0]
        # INTO = params[1]
        table_name = params[2]
        validate_string(table_name, "TABLE")
        self.table = super().metadata.get_table_schema(table_name)
        self.table_store = super().metadata.get_table_store(table_name)

        super().params_values.append(self.table)

        # VALUES = params[3]
        values_str = "".join(params[4:])
        if ('(',')') != (values_str[0], values_str[-1]):
            raise DbCommandException(f"Нарушена семантика передачи значений "
                                     f"на вставку в таблицу: "
                                     f"в выражении '{values_str}' не хватает скобок")

        values = values_str[1:-1].replace(" ","").split(",")
        number_of_columns = len(self.table.column_names)
        number_of_values = len(values)
        if number_of_values != number_of_columns:
            raise DbCommandException(f"Количество значений для вставки ({number_of_values}) "
                                     f"не соответствует количеству колонок ({number_of_columns}) "
                                     f"таблицы '{table_name}'")

        super().params_values.append(values)

    def execute(self) -> List[List[str]]:
        values:List[str]|None = self._get_param_value(1)
        if values is None:
            raise DbCommandException(f"Не зарегистрированы значения "
                                     f"для вставки во внутреннем контексте команды: "
                                     f"{super().params_values}")
        return self.table_store.insert_tuple(values)


