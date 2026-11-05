from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any
import math

class DbDataType(StrEnum):
    """Отображает скалярные типы данных,
    допустимые для обработки в БД"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DATETIME = "datetime"
    BOOLEAN = "bool"

    @classmethod
    def from_string(cls, str_value: str) -> DbDataType:
        cleaned_value = str_value.strip().lower()
        return DbDataType(cleaned_value)

    def validate(self, value: Any) -> bool:
        """Проверяет некоторое значение
        на соответствие типу данных"""
        match self:
            case DbDataType.STRING:
                return True
            case DbDataType.INTEGER:
                str_value = str(value)
                return str_value.lstrip("+-").isdigit()
            case DbDataType.FLOAT:
                try:
                    float(value)
                    return not (math.isinf(value) or
                                math.isnan(value))
                except ValueError:
                    return False
            case DbDataType.DATETIME:
                try:
                    datetime.fromisoformat(str(value))
                    return True
                except ValueError:
                    return False

            case DbDataType.BOOLEAN:
                try:
                    norm_str = str(value).lower().strip()
                    return norm_str == "true" or norm_str == "false"
                except ValueError:
                    return False




