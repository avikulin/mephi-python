from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict

from dz_simple_database_vikulin_m25_555.model.db_datatype import DbDataType
from dz_simple_database_vikulin_m25_555.utils.validation import (
    validate_dict,
    validate_string,
)

COLUMN_NAME = "NAME"
DATATYPE_NAME = "DATATYPE"
IS_MANDATORY_NAME = "IS_MANDATORY"
IS_PRIMARY_NAME = "IS_PRIMARY"


@dataclass(frozen=True)
class DbColumn:
    """Отображает метаданные колонки таблицы:
    1) имя,
    2) тип данных,
    3) признак обязательности
    4) признак участия колонки в первичном ключе записи"""

    name: str
    datatype: DbDataType
    is_mandatory: bool
    is_primary: bool

    def validate_value(self, value: Any):
        return self.datatype.validate(value)

    @property
    def schema(self) -> Dict[str, Any]:
        """Формирует структурированную схему метаданных колонки"""
        data = {
            COLUMN_NAME: self.name,
            DATATYPE_NAME: str(self.datatype),
            IS_MANDATORY_NAME: self.is_mandatory,
            IS_PRIMARY_NAME: self.is_primary,
        }
        return data

    def to_json(self) -> str:
        """Сериализует колонку в JSON."""
        return json.dumps(self.schema, ensure_ascii=False)

    @classmethod
    def from_schema(cls, schema: Dict[str, Any]) -> DbColumn:
        validate_dict(schema, "schema")
        name = validate_string(schema.get(COLUMN_NAME),
                               f"schema['{COLUMN_NAME}']")

        datatype = DbDataType.from_string(
            validate_string(schema.get(DATATYPE_NAME),
                            f"schema['{DATATYPE_NAME}']")
        )

        is_primary = schema.get(IS_PRIMARY_NAME)
        is_mandatory = schema.get(IS_MANDATORY_NAME)

        if not isinstance(is_mandatory, bool):
            raise TypeError(
                f"Параметр 'schema['{IS_MANDATORY_NAME}']' должен быть булевым, "
                f"получен {type(is_mandatory).__name__}"
            )
        if not isinstance(is_primary, bool):
            raise TypeError(
                f"Параметр 'schema['{IS_PRIMARY_NAME}']' должен быть булевым, "
                f"получен {type(is_primary).__name__}"
            )

        return cls(name, datatype, is_mandatory, is_primary)

    @classmethod
    def from_json(cls, source: str) -> DbColumn:
        """Восстанавливает колонку из JSON-строки."""
        validate_string(source, "source")
        try:
            schema = json.loads(source)
            validate_dict(schema, "schema")
            return cls.from_schema(schema)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Параметр 'source' должен быть корректным JSON: {e}"
            ) from None


