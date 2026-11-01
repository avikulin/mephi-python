import copy
from pathlib import Path
from typing import Dict, Any

from dz_simple_database_vikulin_m25_555.io import read_json

CFG_DIR_NAME = "cfg"
DATA_DIR_NAME = "data"
CFG_FILE_NAME = "config.json"


class ConfigError(Exception):
    """Доменное исключение для ошибок конфигурации"""


def check_directory_exists(path: Path, name: str) -> None:
    if not path.exists():
        raise ConfigError(f"Каталог '{name}' не найден: {path}")
    if not path.is_dir():
        raise ConfigError(f"По адресу '{name}' расположен не каталог: {path}")


class DbConfig:
    def __init__(self):
        # корень пакета: config/db_config.py -> на уровень выше
        self.base_dir = Path(__file__).resolve().parents[1]

        # каталог с конфигурационным файлом
        self.cfg_dir = self.base_dir / CFG_DIR_NAME
        check_directory_exists(self.cfg_dir, CFG_DIR_NAME)

        # определяем путь к конфигурационному файлу и читаем его
        self.cfg_file_path = self.cfg_dir / CFG_FILE_NAME
        self.cfg_data = read_json(self.cfg_file_path)

        # определяем каталог для хранения данных
        self.data_dir = self.base_dir / DATA_DIR_NAME
        check_directory_exists(self.data_dir, DATA_DIR_NAME)

    @property
    def base_directory_path(self) -> Path:
        return self.base_dir

    @property
    def data_directory_path(self) -> Path:
        return self.data_dir

    @property
    def config_directory_path(self) -> Path:
        return self.cfg_dir

    @property
    def config_file_path(self) -> Path:
        return self.cfg_file_path

    @property
    def data(self) -> Dict[str, Any]:
        return copy.deepcopy(self.cfg_data)
