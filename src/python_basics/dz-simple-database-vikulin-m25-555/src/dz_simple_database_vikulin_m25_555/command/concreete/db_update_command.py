from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import DbCommandBase, DbCommandException
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import DbCommandParam
from dz_simple_database_vikulin_m25_555.command.expression.db_predicate import DbPredicate
from dz_simple_database_vikulin_m25_555.command.expression.factory.db_predicate_factory import DbPredicateFactory
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import DbMetadataStore
from dz_simple_database_vikulin_m25_555.persistence.table_store.db_table_store import DbTableStore
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbCommandUpdate(DbCommandBase):
    TOKEN_SCHEMA = ("update <имя_таблицы> "
                    "set <столбец> = <новое_значение> "
                    "where [столбец_условия] = [значение_условия]")
    PARAMS_SCHEMA = [
        DbCommandParam(
            "имя_таблицы",
            DbTable,
            "Имя таблицы, в которой будет производиться обновление значений строки",
            True,
        ),
        DbCommandParam(
            "<столбец>",
            str,
            "Название столбца, в котором будут обновляться значения",
            True,
        ),
        DbCommandParam(
            "<новое_значение>",
            str,
            "Значение, которым будут обновлены строки, удовлетворяющие условию",
            True,
        ),
        DbCommandParam(
            "[столбец_условия]=[значение_условия]",
            DbPredicate,
            "Условие (предикат) отбора записей таблицы для выполнения операции",
            True,
        )
    ]

    DESCRIPTION = (
        "Выполняет обновление значений строк в таблице (<имя_таблицы>),\n "
        "заполняя значения заданного столбца (<столбец>) значением <новое_значение> "
        "в тех строках, которые удовлетворяют условию [столбец_условия]=[значение_условия]."
        "Обновленные строки возвращаются в качестве результата выполнения команды."
    )

    RULES = [
        "Столбец для обновления значения (<столбец>) может быть только один",
        "Тип значения <новое_значение> должен соответствовать типу столбца <столбец>",
        "Столбец для проверки условия ([столбец_условия]) может быть только один"
        "Тип значения [значение_условия] должен соответствовать типу столбца [столбец_условия]",
        "Возвращаются все строки, значения которых были обновлены",
        "Возвращаются все колонки обновленных строк, указанные в схеме таблицы",
    ]

    NAME = "update"

    def __init__(self, metadata: DbMetadataStore) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            DbCommandUpdate.TOKEN_SCHEMA,
            DbCommandUpdate.PARAMS_SCHEMA,
            DbCommandUpdate.DESCRIPTION,
            DbCommandUpdate.RULES,
            DbCommandUpdate.NAME
        )
        self.table: DbTable = None
        self.table_store: DbTableStore = None

    def parse_params(self, params: List[str]) -> None:
        """Ожидаем:
        update <имя_таблицы>
        set <столбец> = <новое_значение>
        where [столбец_условия] = [значение_условия]"""
        update_token = params[0].lower()
        if update_token != "update":
            raise DbCommandException("Нарушение семантики команды: UPDATE ...")

        table_name = params[1]
        try:
            validate_string(table_name, "TABLE")
        except Exception:
            raise DbCommandException("Нарушение семантики команды: "
                                     "некорректно задано название целевой таблицы")
        self.table:DbTable = self.metadata.get_table_schema(table_name)
        self.table_store:DbTableStore = self.metadata.get_table_store(table_name)
        self.register_param_value(self.table)

        set_token = params[2].lower()
        if set_token != "set":
            raise DbCommandException("Нарушение семантики команды: UPDATE SET ...")

        normalized_tokens = [token.lower() for token in params]

        try:
            where_token_idx = normalized_tokens.index("where")
            if len(params)-1 == where_token_idx:
                raise ValueError() #нет выражения после 'WHERE'
        except ValueError:
            raise DbCommandException("Нарушение семантики команды: "
                                     "отсутствует выражение WHERE ...")

        try:
            assignment_index = normalized_tokens.index("=")
            if assignment_index > where_token_idx:
                raise ValueError() # это '=' от предиката, который идет дальше
        except ValueError:
            raise DbCommandException("Нарушение семантики команды: "
                                     "отсутствует часть выражения "
                                     "SET <столбец> = <новое_значение> ...")


        assignment_str = "".join(params[3:where_token_idx])
        assignment_lvalue, assignment_rvalue = assignment_str.split("=")
        self.register_param_value(assignment_lvalue)
        self.register_param_value(assignment_rvalue)

        predicate_str = "".join(params[where_token_idx + 1:])
        predicate = DbPredicateFactory.process_predicate(predicate_str, self.table)
        self.register_param_value(predicate)

    def execute(self) -> List[List[str]]:
        column:str = self.get_param_value(1)
        value:str = self.get_param_value(2)
        predicate:DbPredicate = self.get_param_value(3)

        # регистрируем схему результата
        self.result_title = f"В таблице '{self.table.name}' обновлены строки"
        for column_name in self.table.column_names:
            self.register_result_schema_item(column_name)

        return self.table_store.update_tuple(column, value, predicate)