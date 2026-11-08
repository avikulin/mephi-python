import json
import os
from pathlib import Path

from dz_simple_database_vikulin_m25_555.utils.io.db_datetime_encoder import (
    DbDateTimeJSONEncoder,
)


class JsonIOError(Exception):
    """Доменное исключение для ошибок чтения/записи JSON-файлов"""


def read_json(path: Path) -> dict:
    """Читает JSON-файл и возвращает словарь.

    Бросает JsonIOError с понятным описанием для всех
    ожидаемых проблем: файл не найден, нет прав, плохая
    кодировка, невалидный JSON, корень не объект.
    """
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise JsonIOError(f"Файл не найден: {path}") from e
    except PermissionError as e:
        raise JsonIOError(f"Нет прав на чтение файла: {path}") from e
    except UnicodeDecodeError as e:
        raise JsonIOError(f"Ошибка кодировки при чтении файла: {path}") from e
    except OSError as e:
        raise JsonIOError(f"OS-ошибка при чтении файла: {path}") from e
    except json.JSONDecodeError as e:
        raise JsonIOError(f"Ошибка чтения JSON-формата данных в файле: {path}") from e
    if not isinstance(data, dict):
        raise JsonIOError(f"Ожидался JSON-объект в файле: {path}")
    return data


def write_json(path: Path, data: dict) -> None:
    """Записывает словарь в JSON-файл (UTF-8, читаемое форматирование)."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, cls=DbDateTimeJSONEncoder)
    except PermissionError as e:
        raise JsonIOError(f"Нет прав на запись файла: {path}") from e
    except OSError as e:
        raise JsonIOError(f"OS-ошибка при записи файла: {path}") from e
    except TypeError as e:
        raise JsonIOError(
            f"Данные не сериализуются в JSON для файла {path}: {e}"
        ) from e

def drop_file(path: Path) -> None:
    if os.path.exists(path) and not path.is_dir():
        try:
            os.remove(path)
        except PermissionError:
            raise JsonIOError(f"Ошибка: нет прав на удаление файла '{path}'")
        except OSError as e:
            raise JsonIOError(f"Ошибка ОС при удалении файла '{path}': {e}")
    # если файла нет - то просто выходим

def drop_folder(path: Path) -> None:
    if os.path.exists(path) and path.is_dir():
        try:
            os.rmdir(path)
        except PermissionError:
            raise JsonIOError(f"Ошибка: нет прав на удаление каталога '{path}'")
        except OSError as e:
            raise JsonIOError(f"Ошибка ОС при удалении каталога '{path}': {e}")

def touch_file(path: Path, initial_data=None) -> None:
    if initial_data is None:
        initial_data = dict()
    if not os.path.exists(path) and not path.is_dir():
        try:
            write_json(path, initial_data)
        except PermissionError | OSError as e:
            raise JsonIOError(f"Ошибка создания файла '{path}': {e}")