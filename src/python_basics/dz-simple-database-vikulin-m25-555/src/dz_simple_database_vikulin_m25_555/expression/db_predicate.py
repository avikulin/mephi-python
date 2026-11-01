from datetime import datetime
from typing import Union

from dz_simple_database_vikulin_m25_555.expression.db_predicate_operation import (
    DbPredicateOperation,
)
from dz_simple_database_vikulin_m25_555.model.db_column import DbColumn

ORDERING_OPERATIONS = frozenset(
    {
        DbPredicateOperation.GT,
        DbPredicateOperation.GE,
        DbPredicateOperation.LT,
        DbPredicateOperation.LE,
    }
)


class DbPredicate:
    def __init__(
        self,
        column: DbColumn,
        op: DbPredicateOperation,
        value: Union[str, bool, int, float, datetime],
    ):
        self.column = column
        self.operation = op
        if not self.column.datatype.validate(value):
            raise ValueError(
                f"Значение {value} не соответствует типу данных "
                f"'{self.column.datatype}' поля '{self.column.name}'"
            )
        if isinstance(value, bool) and op in ORDERING_OPERATIONS:
            raise ValueError(
                f"Операция '{op}' не применима к логическому типу "
                f"поля '{self.column.name}'"
            )
        self.value = value

    def apply(self, field_data: Union[str, bool, int, float, datetime]) -> bool:
        match self.operation:
            case DbPredicateOperation.EQ:
                return field_data == self.value

            case DbPredicateOperation.NEQ:
                return field_data != self.value

            case DbPredicateOperation.GT:
                return field_data > self.value

            case DbPredicateOperation.GE:
                return field_data >= self.value

            case DbPredicateOperation.LT:
                return field_data < self.value

            case DbPredicateOperation.LE:
                return field_data <= self.value
