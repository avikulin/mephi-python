from dataclasses import dataclass
from typing import Any


@dataclass
class DbCommandParam:
    name: str
    type_ref: type
    description: str
    is_mandatory: bool

    def check_type(self, value: Any) -> bool:
        """Проверяет тип параметра"""
        return isinstance(value, self.type_ref)

    def describe(self):
        """Строит структурированное человекочитаемое описание параметра"""
        mandatory = "да" if self.is_mandatory else "нет"
        return (f"<{self.name}>. {self.description} "
                f"(тип: {self.type_ref}, "
                f"обязательность: {mandatory})")