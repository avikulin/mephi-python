from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from dz_simple_database_vikulin_m25_555.model.db_datatype import DbDataType
from dz_simple_database_vikulin_m25_555.validation import validate_dict, validate_string

COLUMN_NAME = "NAME"
DATATYPE_NAME = "DATATYPE"
IS_MANDATORY_NAME = "IS_MANDATORY"
IS_PRIMARY_NAME = "IS_PRIMARY"


@dataclass(frozen=True)
class DbColumn:
    """Отображает метаданные колонки таблицы:
    1) имя,
    2) тип данных,
    3) признак обязательности"""

    name: str
    datatype: DbDataType
    is_mandatory: bool
    is_primary: bool

    def validate_value(self, value: Any):
        return self.datatype.validate(value)

    def to_json(self) -> str:
        """Сериализует колонку в JSON."""
        data = {
            COLUMN_NAME: self.name,
            DATATYPE_NAME: str(self.datatype),
            IS_MANDATORY_NAME: self.is_mandatory,
            IS_PRIMARY_NAME: self.is_primary,
        }
        return json.dumps(data, ensure_ascii=False)

    @classmethod
    def from_json(cls, source: str) -> DbColumn:
        """Восстанавливает колонку из JSON-строки."""
        validate_string(source, "source")
        try:
            data = json.loads(source)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Параметр 'source' должен быть корректным JSON: {e}"
            ) from None
        validate_dict(data, "data")
        name = validate_string(data.get(COLUMN_NAME), f"data['{COLUMN_NAME}']")
        datatype = DbDataType.from_string(
            validate_string(data.get(DATATYPE_NAME), f"data['{DATATYPE_NAME}']")
        )
        is_mandatory = data.get(IS_MANDATORY_NAME)
        is_primary = data.get(IS_PRIMARY_NAME)
        if not isinstance(is_mandatory, bool):
            raise TypeError(
                f"Параметр 'data['{IS_MANDATORY_NAME}']' должен быть булевым, "
                f"получен {type(is_mandatory).__name__}"
            )
        if not isinstance(is_primary, bool):
            raise TypeError(
                f"Параметр 'data['{IS_PRIMARY_NAME}']' должен быть булевым, "
                f"получен {type(is_primary).__name__}"
            )
        return cls(name, datatype, is_mandatory, is_primary)
