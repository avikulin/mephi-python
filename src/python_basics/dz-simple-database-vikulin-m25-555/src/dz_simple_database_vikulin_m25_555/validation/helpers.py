

def validate_not_empty(value: list | dict | None, name: str) -> None:
    """Проверка общего случая: значение не None и не пустое."""
    if value is None:
        raise ValueError(f"Параметр '{name}' не должен быть None")
    if len(value) == 0:
        raise ValueError(f"Параметр '{name}' не должен быть пустым")

def validate_string(value: str | None, name: str) -> str:
    """Строка не None и не пустая (пробелы тоже считаются пустотой)."""
    if value is None:
        raise ValueError(f"Параметр '{name}' не должен быть None")
    if not isinstance(value, str):
        raise TypeError(f"Параметр '{name}' должен быть строкой, получен {type(value).__name__}")
    if not value.strip():
        raise ValueError(f"Параметр '{name}' не должен быть пустой строкой")
    return value

def validate_list(value: list | None, name: str) -> list:
    if value is None:
        raise ValueError(f"Параметр '{name}' не должен быть None")
    if not isinstance(value, list):
        raise TypeError(f"Параметр '{name}' должен быть списком, получен {type(value).__name__}")
    if not value:
        raise ValueError(f"Список '{name}' не должен быть пустым")
    return value

def validate_dict(value: dict | None, name: str) -> dict:
    if value is None:
        raise ValueError(f"Параметр '{name}' не должен быть None")
    if not isinstance(value, dict):
        raise TypeError(f"Параметр '{name}' должен быть словарём, получен {type(value).__name__}")
    if not value:
        raise ValueError(f"Словарь '{name}' не должен быть пустым")
    return value