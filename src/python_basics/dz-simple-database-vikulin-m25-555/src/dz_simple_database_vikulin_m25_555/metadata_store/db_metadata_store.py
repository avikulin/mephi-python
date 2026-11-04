from pathlib import Path
from typing import Dict, Tuple

from dz_simple_database_vikulin_m25_555.config.db_config import DbConfig
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable, PKEY_NAME
from dz_simple_database_vikulin_m25_555.table_store.db_table_store import DbTableStore
from dz_simple_database_vikulin_m25_555.utils.io import read_json, write_json, JsonIOError
from dz_simple_database_vikulin_m25_555.utils.io.json_io import drop_file, touch_file
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string

SCHEMA_FILE_NAME = "schema.json"
DATA_FILE_NAME = "data.json"
METADATA_FILE_PATH = "metadata_catalog.json"

DATA_FILE_PATH_KEY = "DATA"
SCHEMA_FILE_PATH_KEY = "SCHEMA"

class DbMetadataException(Exception):
    """Доменное исключение работы с метаданными БД"""

class DbMetadataStore:
    def __init__(self, global_cfg: DbConfig):
        self.config = global_cfg
        self.metadata_file_name = self.config.data_directory_path / METADATA_FILE_PATH
        self.arena = {}
        self.metadata_index = {}
        self.store_index = {}

    def _restore_state(self):
        try:
            touch_file(self.metadata_file_name) # создаем файл, если его не было
            data = read_json(self.metadata_file_name)  # читаем из файла
        except JsonIOError as e:
            raise DbMetadataException(f"Ошибка чтения файла каталога метаданных "
                                      f"'{self.metadata_file_name}': {e}") from e
        try:
            for table_name, table_data in data.items():
                data_file_path = table_data[DATA_FILE_PATH_KEY]
                schema_file_path = table_data[SCHEMA_FILE_PATH_KEY]
                self.arena[table_name] = {
                    Path(data_file_path),
                    Path(schema_file_path)
                }
                table_schema = self._construct_table_schema(schema_file_path)
                self.metadata_index[table_name] = table_schema
                self.store_index[table_name] = DbTableStore(table_schema,
                                                            data_file_path,
                                                            self.config)
        except ValueError as e:
            raise DbMetadataException(f"Ошибка формата файла каталога метаданных "
                                      f"'{self.metadata_file_name}': {e}") from e

    def _ensure_table_exists(self,name:str) -> None:
        validate_string(name, "name")
        if name not in self.metadata_index:
            raise DbMetadataException(f"Таблица '{name}' не зарегистрирована в БД")

    def _construct_paths(self, name: str) -> Tuple[Path, Path]:
        data_file_path = self.config.data_directory_path / name / DATA_FILE_NAME
        schema_file_path = self.config.data_directory_path / name / SCHEMA_FILE_NAME
        return data_file_path, schema_file_path

    def _construct_table_schema(self, schema_file_path: Path) -> DbTable:
        try:
            schema_json = read_json(schema_file_path)
            return DbTable.from_json(schema_json)
        except JsonIOError as e:
            raise DbMetadataException(f"Ошибка чтения файла схемы таблицы: "
                                      f"'{schema_file_path}': {e}") from e


    def _flush_arena(self):
        try:
            write_json(self.metadata_file_name, self.arena)
        except JsonIOError as e:
            raise DbMetadataException(f"Ошибка записи файла каталога метаданных "
                                      f"'{self.metadata_file_name}': {e}") from e

    def register_table(self, name:str, schema: Dict[str, str]):
        if PKEY_NAME in schema:
            raise DbMetadataException("Недопустимо указывать системный "
                                      "столбец ID в перечне бизнес-полей")

        if name in self.arena:
            raise DbMetadataException(f"Таблица '{name}' уже зарегистрирована в БД")

        data_file_path, schema_file_path = self._construct_paths(name)
        try:
            table = DbTable.from_schema(name, schema)
            write_json(schema_file_path, table.metadata)
        except DbMetadataException as e:
            raise DbMetadataException(f"Ошибка обработки схемы столбцов: {e}") from e
        except JsonIOError as e:
            raise DbMetadataException(f"Ошибка записи схемы таблицы в файл: "
                                      f"{schema_file_path}.{e}")
        # если дошли до сюда - значит можно модифицировать внутреннее состояние
        self.arena[name] = {
            DATA_FILE_PATH_KEY: data_file_path,
            SCHEMA_FILE_PATH_KEY: schema_file_path
        }
        self.metadata_index[name] = table
        self.store_index[name] = DbTableStore(table, data_file_path, self.config)
        self._flush_arena()
        return table

    def drop_table(self, name:str):
        if name not in self.arena:
            raise DbMetadataException(f"Таблицы с именем '{name}' нет в схеме данных")
        _, schema_file_path = self._construct_paths(name)
        try:
            drop_file(schema_file_path)
        except JsonIOError as e:
            raise DbMetadataException(f"Ошибка удаления файла схемы таблицы '{name}': "
                                      f"'{schema_file_path}'. Детали ошибки: {e}") \
                                      from e
        # если дошли до сюда - значит можно модифицировать внутреннее состояние
        self.arena.pop(name)
        self._flush_arena()

    def get_table_schema(self, name:str) -> DbTable:
        self._ensure_table_exists(name)
        return self.metadata_index[name]

    def get_table_store(self, name:str) -> DbTableStore:
        self._ensure_table_exists(name)
        return self.store_index[name]