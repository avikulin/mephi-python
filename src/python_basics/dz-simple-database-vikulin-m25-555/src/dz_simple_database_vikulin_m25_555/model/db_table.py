from __future__ import annotations

import json

from dz_simple_database_vikulin_m25_555.model.db_column import DbColumn
from dz_simple_database_vikulin_m25_555.model.db_datatype import DbDataType
from dz_simple_database_vikulin_m25_555.validation import (
    validate_dict,
    validate_list,
    validate_string,
)

PKEY_NAME = "ID"
TABLE_NAME = "NAME"
COLUMNS_NAME = "COLUMNS"


class DbTable:
    name: str
    columns: list[DbColumn]

    def __init__(self, name: str, columns: list[DbColumn]):
        validate_string(name, "name")
        validate_list(columns, "columns")
        self._name = name
        self._columns: list[DbColumn] = [
            DbColumn(PKEY_NAME, DbDataType.INTEGER, True, True)
        ]
        for column in columns:
            if not isinstance(column, DbColumn):
                raise TypeError(
                    f"Элементы 'columns' должны быть DbColumn, "
                    f"получен {type(column).__name__}"
                )
            if column.is_primary:
                raise ValueError(
                    f"Колонка '{column.name}' не должна быть primary: "
                    f"первичный ключ создаётся автоматически"
                )
            self._columns.append(column)

    @classmethod
    def from_schema(cls, name: str, columns: dict[str, str]) -> DbTable:
        """Создаёт таблицу из схемы: имя колонки → строковое имя типа данных."""
        validate_string(name, "name")
        validate_dict(columns, "columns")
        if not columns:
            raise ValueError("Параметр 'columns' не должен быть пустым")
        restored = [
            DbColumn(k, DbDataType.from_string(v), False, False)
            for k, v in columns.items()
        ]
        return cls(name, restored)

    @classmethod
    def from_columns(cls, name: str, columns: list[DbColumn]) -> DbTable:
        """Создаёт таблицу из готовых колонок."""
        return cls(name, columns)

    @property
    def name(self):
        return self._name

    @property
    def pkey(self) -> DbColumn:
        return self._columns[0]

    @property
    def column_names(self) -> list[str]:
        return [column.name for column in self._columns]

    @property
    def columns(self) -> list[DbColumn]:
        return list(self._columns)

    @property
    def metadata(self) -> dict:
        """Метаданные таблицы.
        В COLUMNS попадают все колонки (в т.ч. и первичный ключ).
        """
        return {
            TABLE_NAME: self.name,
            COLUMNS_NAME: [column for column in self._columns],
        }

    def to_json(self) -> str:
        """Сериализует таблицу в JSON на основе metadata."""
        metadata = self.metadata
        metadata[COLUMNS_NAME] = [
            json.loads(column.to_json()) for column in metadata[COLUMNS_NAME]
        ]
        return json.dumps(metadata, ensure_ascii=False)

    @classmethod
    def from_json(cls, source: str) -> DbTable:
        """Восстанавливает таблицу из JSON-строки."""
        validate_string(source, "source")
        try:
            data = json.loads(source)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Параметр 'source' должен быть корректным JSON: {e}"
            ) from None
        validate_dict(data, "data")
        name = validate_string(data.get(TABLE_NAME), f"data['{TABLE_NAME}']")
        columns = data.get(COLUMNS_NAME)
        if not isinstance(columns, list):
            raise TypeError(
                f"Параметр 'data['{COLUMNS_NAME}']' должен быть списком, "
                f"получен {type(columns).__name__}"
            )
        if not columns:
            raise ValueError("Таблица должна содержать хотя бы одну колонку")
        restored = [DbColumn.from_json(json.dumps(item)) for item in columns]
        expected_pkey = DbColumn(PKEY_NAME, DbDataType.INTEGER, True, True)
        primaries = [c for c in restored if c.is_primary]
        if primaries != [expected_pkey]:
            raise ValueError(
                f"Первичный ключ в JSON должен быть "
                f"{expected_pkey!s}, получен: {primaries!s}"
            )
        business = [c for c in restored if not c.is_primary]
        if not business:
            raise ValueError(
                "Таблица должна содержать хотя бы одну колонку "
                "с бизнес-данными помимо первичного ключа"
            )
        return cls(name, business)
