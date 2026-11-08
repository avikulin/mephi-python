from typing import Tuple

from dz_simple_database_vikulin_m25_555.command.expression.db_predicate import (
    DbPredicate,
)
from dz_simple_database_vikulin_m25_555.command.expression.db_predicate_operation import (
    DbPredicateOperation,
    DbPredicateOperationException,
)
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.persistence.table_store.db_table_store import (
    DbValueConstructor,
)
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbPredicateFactory:

    @classmethod
    def construct_predicate(cls, lvalue:str, op:str, rvalue:str, table: DbTable):
        validate_string(lvalue, "lvalue")
        validate_string(op, "op")
        validate_string(rvalue, "rvalue")

        column = table.get_column(lvalue)
        data_type = column.datatype
        typed_criteria = DbValueConstructor.construct(rvalue, data_type)
        operation = DbPredicateOperation.from_string(op)
        return DbPredicate(column, operation, typed_criteria)