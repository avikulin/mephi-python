import copy
import re
from typing import Dict, List, Callable

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import (
    DbCommandBase,
    DbCommandException,
)
from dz_simple_database_vikulin_m25_555.persistence.metadata_store.db_metadata_store import DbMetadataStore
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string

class DbCommandFactoryException(Exception):
    """Доменное исключение для обработки ошибок фабрики команд"""
    pass

class DbCommandFactory:
    def __init__(self, metadata: DbMetadataStore):
        if metadata is None:
            raise
        self.class_catalog:Dict[re.Pattern, Callable[[DbMetadataStore], DbCommandBase]] = {}
        self.name_catalog:List[str] = []
        self.metadata = metadata

    def register_command(self, pattern:str,
                         command_class:Callable[[DbMetadataStore], DbCommandBase]) -> None:
        """Выполняет регистрацию команду и regex-паттерна ее классификация.
        Паттерн должен быть составлен для уникальной классификации данной команды"""
        validate_string(pattern, "pattern")
        if command_class is None:
            raise DbCommandException("Не допускается регистрация "
                                     "пустой ссылки на команду БД")

        regex = re.compile(pattern, re.IGNORECASE)
        self.class_catalog[regex] = command_class

        # получим внутреннее имя
        temp_cmd = command_class(self.metadata)
        self.name_catalog.append(temp_cmd.name)

    def get_command(self, command_string:str) -> DbCommandBase:
        """Возвращает единственную команду,
        подходящую под зарегистрированные паттерны"""
        for pattern, command_class_ref in self.class_catalog.items():
            match = pattern.match(command_string)
            if match:
                return command_class_ref(self.metadata)
        raise DbCommandException(f"Не найдено подходящего шаблона "
                                 f"обработки для переданной команды: "
                                 f"{command_string}")

    @property
    def all_commands(self) -> List[DbCommandBase]:
        """Возвращает полный список зарегистрированных команд БД"""
        return [cmd(self.metadata) for cmd in self.class_catalog.values()]

    @property
    def all_command_names(self) -> List[str]:
        """Возвращает структуру (имя:команда)"""
        return copy.deepcopy(self.name_catalog)