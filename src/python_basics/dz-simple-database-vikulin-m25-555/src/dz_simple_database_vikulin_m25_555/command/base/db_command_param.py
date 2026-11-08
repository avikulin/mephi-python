from dataclasses import dataclass
from typing import Any, get_origin

from dz_simple_database_vikulin_m25_555.utils.console.db_console_colors import Color


@dataclass
class DbCommandParam:
    name: str
    type_ref: type
    description: str
    is_mandatory: bool

    def check_type(self, value: Any) -> bool:
        """Проверяет тип параметра.
        Поддерживает параметризованные generics (например, List[str])"""
        type_ref = get_origin(self.type_ref) or self.type_ref #тут Алиса помогла))
        return isinstance(value, type_ref)

    def describe(self):
        """Строит структурированное человекочитаемое описание параметра"""
        mandatory = "да" if self.is_mandatory else "нет"
        return (
            f"{Color.OKCYAN}<{self.name}>{Color.ENDC}. {self.description} "
            f"(тип: {Color.OKCYAN}{self.type_ref.__name__}{Color.ENDC}, "
            f"обязательность: {Color.OKCYAN}{mandatory}{Color.ENDC})"
        )
