from __future__ import annotations

from enum import StrEnum


class DbPredicateOperationException(Exception):
    """Доменное исключение для работы с предикатами"""

class DbPredicateOperation (StrEnum):
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="
    EQ = "="
    NEQ = "!="

    @classmethod
    def from_string(cls, value:str) -> DbPredicateOperation:
        cleaned_value = value.strip().lower()
        return DbPredicateOperation(cleaned_value)