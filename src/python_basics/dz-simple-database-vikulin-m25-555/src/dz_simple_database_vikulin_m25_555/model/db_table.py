from __future__ import annotations

import json
from typing import Any, Dict, Union, List

from dz_simple_database_vikulin_m25_555.model.db_column import DbColumn
from dz_simple_database_vikulin_m25_555.model.db_datatype import DbDataType
from dz_simple_database_vikulin_m25_555.utils.validation import (
    validate_dict,
    validate_list,
    validate_string,
)

PKEY_NAME = "ID"
TABLE_NAME = "NAME"
COLUMNS_NAME = "COLUMNS"

class DbTableOperationException(Exception):
    """Доменное исключение для операций с таблицами"""


class DbTable:
    name: str
    columns: list[DbColumn]

    def __init__(self, name: str, columns: list[DbColumn]):
        validate_string(name, "name")
        validate_list(columns, "columns")
        self._name = name
        pkey = DbColumn(PKEY_NAME, DbDataType.INTEGER, True, True)
        self._columns: list[DbColumn] = [pkey]
        self._column_index = {pkey.name.lower() : pkey}
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
            self._column_index[column.name.lower()] = column

    def get_column(self, name: str) -> DbColumn:
        """Ищет объект DbColumn по имени (без учета регистра)"""
        validate_string(name, "name")
        column = self._column_index[name.lower()]
        if column is None:
            raise DbTableOperationException(f"В схеме таблицы нет колонки '{name}'")
        return column

    @classmethod
    def from_schema(cls, name: str, columns: Dict[str, str]) -> DbTable:
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
        return [column.name.lower() for column in self._columns]

    @property
    def columns(self) -> list[DbColumn]:
        return list(self._columns)

    @property
    def metadata(self) -> Dict[str,Union[str, List[DbColumn]]]:
        """Метаданные таблицы.
        В COLUMNS попадают все колонки (в т.ч. и первичный ключ).
        """
        return {
            TABLE_NAME: self.name,
            COLUMNS_NAME: [column for column in self._columns],
        }

    @property
    def schema(self)->Dict[str, Any]:
        """Формирует структурированную схему таблицы"""
        return {
            column.name: column.datatype
            for column in self.metadata[COLUMNS_NAME]
        }

    def to_json(self) -> str:
        """Сериализует таблицу в JSON на основе metadata."""
        metadata = self.metadata
        metadata[COLUMNS_NAME] = [
            json.loads(column.to_json()) for column in metadata[COLUMNS_NAME]
        ]
        return json.dumps(metadata, ensure_ascii=False)

    @classmethod
    def from_json(cls, source: Dict[str, Any]) -> DbTable:
        """Восстанавливает таблицу из JSON-строки."""
        validate_dict(source, "source")
        if TABLE_NAME not in source:
            raise DbTableOperationException(f"Неправильный формат источника: "
                                            f"отсутствует поле '{TABLE_NAME}'")

        if COLUMNS_NAME not in source:
            raise DbTableOperationException(f"Неправильный формат источника: "
                                            f"отсутствует поле '{COLUMNS_NAME}'")
        table_name = source[TABLE_NAME]
        columns = source[COLUMNS_NAME]
        return DbTable.from_schema(table_name, columns)
