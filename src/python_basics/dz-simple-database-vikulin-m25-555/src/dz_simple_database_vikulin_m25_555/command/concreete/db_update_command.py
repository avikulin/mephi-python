from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import (
    DbCommandBase,
    DbCommandException,
)
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import (
    DbCommandParam,
)
from dz_simple_database_vikulin_m25_555.command.expression.db_predicate import (
    DbPredicate,
)
from dz_simple_database_vikulin_m25_555.command.expression.factory.db_predicate_factory import (
    DbPredicateFactory,
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
            "столбец",
            str,
            "Название столбца, в котором будут обновляться значения",
            True,
        ),
        DbCommandParam(
            "новое_значение",
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
        f"Выполняет обновление значений строк в таблице "
        f"{Color.OKCYAN}(<имя_таблицы>){Color.ENDC},\n"
        f"заполняя значения заданного столбца {Color.OKCYAN}(<столбец>){Color.ENDC} "
        f"значением {Color.OKCYAN}<новое_значение>{Color.ENDC}\n"
        f"в тех строках, которые удовлетворяют условию "
        f"{Color.OKCYAN}[столбец_условия]=[значение_условия]{Color.ENDC}.\n"
        "Обновленные строки возвращаются в качестве результата выполнения команды."
    )

    RULES = [
        f"{Color.OKCYAN}<столбец>{Color.ENDC} для обновления значения "
        f" может быть только один",
        f"Тип значения {Color.OKCYAN}<новое_значение>{Color.ENDC} должен "
        f"соответствовать типу столбца <столбец>",
        f"Столбец для проверки условия {Color.OKCYAN}[столбец_условия]{Color.ENDC}"
        f" может быть только один",
        f"Тип значения {Color.OKCYAN}[значение_условия]{Color.ENDC} должен "
        f"соответствовать типу столбца {Color.OKCYAN}[столбец_условия]{Color.ENDC}",
        "Возвращаются все строки, значения которых были обновлены",
        "Возвращаются все колонки обновленных строк, указанные в схеме таблицы",
    ]

    NAME = "update"

    CMD_SET_TOKEN = "set"
    CMD_WHERE_TOKEN = "where"

    NOT_FOUND_IDX = -1

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
        update_token = params[0].strip().lower()
        if update_token != "update":
            raise DbCommandException("Нарушение семантики команды: UPDATE ...")

        table_name = params[1].strip().lower()
        validate_string(table_name, "TABLE")

        self.table:DbTable = self.metadata.get_table_schema(table_name)
        self.table_store:DbTableStore = self.metadata.get_table_store(table_name)
        self.register_param_value(self.table)

        cmd_set_token_idx = DbCommandUpdate.NOT_FOUND_IDX
        cmd_where_token_idx = DbCommandUpdate.NOT_FOUND_IDX
        set_pattern = DbCommandUpdate.CMD_SET_TOKEN
        where_pattern = DbCommandUpdate.CMD_WHERE_TOKEN

        for i in range(2, len(params)):
            token = params[i].strip().lower()
            if token.find(set_pattern) != DbCommandUpdate.NOT_FOUND_IDX:
                cmd_set_token_idx = i
            if token.find(where_pattern) != DbCommandUpdate.NOT_FOUND_IDX:
                cmd_where_token_idx = i

        # проверяем, что оба токена найдены и после WHERE что-то есть
        if (cmd_set_token_idx == DbCommandUpdate.NOT_FOUND_IDX or
            cmd_where_token_idx == DbCommandUpdate.NOT_FOUND_IDX or
            cmd_where_token_idx == len(params) - 1):
            raise DbCommandException("Нарушение семантики команды: UPDATE SET ...")

        set_expr_str = " ".join(params[cmd_set_token_idx: cmd_where_token_idx])
        where_expr_str = " ".join(params[cmd_where_token_idx:])

        target_column, target_value = ParseExprHelper.parse_assignment(
            set_expr_str,
            DbCommandUpdate.CMD_SET_TOKEN,
            None,
            "set <столбец> = <новое_значение>")

        p_column, p_op, p_rvalue = ParseExprHelper.parse_predicate(
            where_expr_str,
            DbCommandUpdate.CMD_WHERE_TOKEN,
            None,
           " where [столбец_условия] = [значение_условия]")

        self.register_param_value(target_column)
        self.register_param_value(target_value)

        predicate = DbPredicateFactory.construct_predicate(p_column, p_op, p_rvalue, self.table)
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