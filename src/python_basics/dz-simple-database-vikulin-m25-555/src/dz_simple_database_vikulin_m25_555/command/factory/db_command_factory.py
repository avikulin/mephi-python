import re
from typing import List

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import DbCommandBase, DbCommandException
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbCommandFactory:
    def __init__(self):
        self.catalog = {}

    def register_command(self, pattern:str, command:DbCommandBase) -> None:
        """Выполняет регистрацию команду и regex-паттерна ее классификация.
        Паттерн должен быть составлен для уникальной классификации данной команды"""
        validate_string(pattern, "pattern")
        if command is None:
            raise DbCommandException("Не допускается регистрация "
                                     "пустой ссылки на команду БД")
        regex = re.compile(pattern, re.IGNORECASE)
        self.catalog[regex] = command

    def get_command(self, command_string:str) -> DbCommandBase:
        """Возвращает единственную команду,
        подходящую под зарегистрированные паттерны"""
        for pattern, command_ref in self.catalog.items():
            match = pattern.match(command_string)
            if len(match.groups()) > 0:
                return command_ref
        raise DbCommandException(f"Не найдено подходящего шаблона "
                                 f"обработки для переданной команды: "
                                 f"{command_string}")

    @property
    def all_commands(self) -> List[DbCommandBase]:
        """Возвращает полный список зарегистрированных команд БД"""
        return [ cmd for cmd in self.catalog.values() ]