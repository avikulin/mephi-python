from typing import Any, Dict

from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from validation.helpers import validate_dict, validate_string

class DbEngine:
    DATA_CATALOG = "/data"
    METADATA_STORE = "schema.json"
    TUPLES_STORE = "data.json"

    metadata: Dict[str, DbTable] = None

    def __init__(self):
        pass

    @classmethod
    def create_table(cls, table_name:str, columns:Dict[str,str]) -> Dict[str, DbTable]:
        """Создает таблицу в пространстве данных БД:
        1. Принимает текущие метаданные, имя таблицы и список столбцов.
        2. Автоматически добавляет столбец ID:int в начало списка столбцов.
        3. Проверяет, не существует ли уже таблица с таким именем. Если да, выводить ошибку.
        4. Проверяет корректность типов данных (только int, str, bool).
        Если все внутренние проверки прошли без ошибок - обновляет словарь metadata и возвращать его."""
        validate_dict(metadata, "metadata")
        validate_string(table_name, "table_name")
        validate_dict(columns, "columns")
        table = DbTable.from_schema(table_name, columns)
        metadata[table_name] = table
        return metadata

    @classmethod
    def drop_table(cls, metadata:Dict[str, DbTable], table_name:str) -> Dict[str, DbTable]:
        """Удаляет таблицу из пространства данных БД:
        1. Проверяет существование таблицы. Если таблицы нет, выводит ошибку.
        2. Удаляет информацию о таблице из metadata и возвращает обновленный словарь."""
        validate_dict(metadata, "metadata")
        validate_string(table_name, "table_name")
        if not table_name in metadata:
            raise ValueError(f"There is no table '{table_name}' in the database schema")
        metadata.pop(table_name)
        return metadata

    @classmethod
    def list_tables(cls, metadata:Dict[str, DbTable]):
        """Выводит список таблиц схемы данных"""
        validate_dict(metadata, "metadata")
        return metadata.keys()

    def load(self) -> Dict[str, Any]:
        pass

    def flush(self, metadata: Dict[str, Any]):
        pass