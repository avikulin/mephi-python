from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any


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
        for dt in DbDataType:
            if cleaned_value == dt.value:
                return dt
        raise ValueError(f"Unsupported datatype: {str_value}")

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
                    return ("inf" not in value and
                            "nan" not in value.lower())
                except ValueError:
                    return False
            case DbDataType.DATETIME:
                try:
                    datetime.fromisoformat(value)
                    return True
                except ValueError:
                    return False

            case DbDataType.BOOLEAN:
                try:
                    norm_str = str(value).lower().strip()
                    return norm_str == "true" or norm_str == "false"
                except ValueError:
                    return False




