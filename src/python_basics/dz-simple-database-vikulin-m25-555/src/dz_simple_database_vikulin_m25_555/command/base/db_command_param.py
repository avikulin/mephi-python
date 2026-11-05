from dataclasses import dataclass
from typing import Any, get_origin


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
            f"<{self.name}>. {self.description} "
            f"(тип: {self.type_ref}, "
            f"обязательность: {mandatory})"
        )
