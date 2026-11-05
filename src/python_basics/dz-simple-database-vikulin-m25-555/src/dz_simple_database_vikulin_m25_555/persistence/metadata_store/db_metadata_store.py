from pathlib import Path
from typing import Dict, Tuple

from dz_simple_database_vikulin_m25_555.config.db_config import DbConfig
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable, PKEY_NAME
from dz_simple_database_vikulin_m25_555.persistence.table_store.db_table_store import DbTableStore
from dz_simple_database_vikulin_m25_555.utils.io import read_json, write_json, JsonIOError
from dz_simple_database_vikulin_m25_555.utils.io.json_io import drop_file, touch_file, drop_folder
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
        self._restore_state()

    def _restore_state(self):
        try:
            touch_file(self.metadata_file_name) # создаем файл, если его не было
            data = read_json(self.metadata_file_name)  # читаем из файла
        except JsonIOError as e:
            raise DbMetadataException(f"Ошибка чтения файла каталога метаданных "
                                      f"'{self.metadata_file_name}': {e}") from e
        try:
            for table_name, table_data in data.items():
                data_file_path = Path(table_data[DATA_FILE_PATH_KEY])
                schema_file_path = Path(table_data[SCHEMA_FILE_PATH_KEY])
                self.arena[table_name] = {
                    data_file_path,
                    schema_file_path
                }
                table_schema = self._construct_table_schema(table_name,
                                                            schema_file_path)
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

    def _construct_db_folder(self, name:str) -> Path:
        validate_string(name, "name")
        return self.config.data_directory_path / name

    def _construct_paths(self, name: str) -> Tuple[Path, Path]:
        validate_string(name, "name")
        db_folder = self._construct_db_folder(name)
        data_file_path = db_folder / DATA_FILE_NAME
        schema_file_path = db_folder / SCHEMA_FILE_NAME
        return data_file_path, schema_file_path

    def _construct_table_schema(self, table_name:str, schema_file_path: Path) -> DbTable:
        try:
            schema_json = read_json(schema_file_path)
            # убираем ID из зачитанных колонок:
            # DbTable добавит этот столбец имплицитно
            cleaned_schema = {k:v for k,v in schema_json.items() if k != PKEY_NAME}
            return DbTable.from_schema(table_name, cleaned_schema)
        except JsonIOError as e:
            raise DbMetadataException(f"Ошибка чтения файла схемы таблицы: "
                                      f"'{schema_file_path}': {e}") from e


    def _flush_arena(self):
        try:
            data_to_flush = {}
            for name, data in self.arena.items():
                table_meta = {
                    DATA_FILE_PATH_KEY: str(data[DATA_FILE_PATH_KEY]),
                    SCHEMA_FILE_PATH_KEY: str(data[SCHEMA_FILE_PATH_KEY]),
                }
                data_to_flush[name] = table_meta

            write_json(self.metadata_file_name, data_to_flush)
        except JsonIOError as e:
            raise DbMetadataException(f"Ошибка записи файла каталога метаданных "
                                      f"'{self.metadata_file_name}': {e}") from e

    def check_table_exists(self, name:str) -> bool:
        """Проверяет наличие таблицы в схеме данных БД"""
        validate_string(name, "name")
        return self.arena.get(name) is not None

    def register_table(self, name:str, schema: Dict[str, str]):
        if PKEY_NAME in schema:
            raise DbMetadataException("Недопустимо указывать системный "
                                      "столбец ID в перечне бизнес-полей")

        if name in self.arena:
            raise DbMetadataException(f"Таблица '{name}' уже зарегистрирована в БД")

        data_file_path, schema_file_path = self._construct_paths(name)
        try:
            table = DbTable.from_schema(name, schema)
            write_json(schema_file_path, table.schema)
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

        db_folder = self._construct_db_folder(name)
        data_file_path, schema_file_path = self._construct_paths(name)
        try:
            drop_file(data_file_path)
            drop_file(schema_file_path)
            drop_folder(db_folder)

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