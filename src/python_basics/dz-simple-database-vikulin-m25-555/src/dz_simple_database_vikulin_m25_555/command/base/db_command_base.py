import copy
import shlex
from datetime import datetime
from typing import List, Union, Any

from dz_simple_database_vikulin_m25_555.command.base.db_command_param import DbCommandParam
from dz_simple_database_vikulin_m25_555.metadata_store.db_metadata_store import DbMetadataStore
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string, validate_list

class DbCommandException(Exception):
    """Доменное исключение для команд БД"""

class DbCommandBase:
    def __init__(self, metadata: DbMetadataStore,
                       token_schema:str,
                       params_schema:List[DbCommandParam],
                       description:str,
                       rules:List[str]):

        # проверка и инициализация ссылки на хранилище метаданных
        if metadata is None:
            raise DbCommandException("Отсутствует ссылка на "
                                     "хранилище метаданных БД (metadata)")
        self.metadata = metadata

        # проверка ключевых параметров,
        # которые будут передаваться из наследников
        validate_string(token_schema, "token_schema")
        validate_list(params_schema, "param_schema")
        validate_string(description, "description")
        validate_list(rules, "rules")

        # инициализация
        self.token_schema = token_schema
        self.params_schema = params_schema
        self.description = description
        self.rules = rules
        self.params_values = []

    def get_help(self) -> str:
        """Получение структурированной справочной информации по команде"""
        params_str = []
        for idx, param in enumerate(self.params_schema):
            params_str.append(f"\t{idx}) {param.describe()}")

        rules_str = []
        for idx, rule in enumerate(self.rules):
            rules_str.append(f"\t{idx}) {rule}")

        pretty_string = (f"{self.token_schema}"
                         f""
                         f"{self.description}."
                         f""
                         f"Спецификация параметров вызова:"
                         f"{"\n".join(params_str)}"
                         f""
                         f"Особенности применения:"
                         f"{"\n".join(rules_str)}"
                         f"")

        return pretty_string

    def get_params_schema(self) -> List[DbCommandParam]:
        """Возвращает список типизированных параметров"""
        return copy.deepcopy(self.params_schema)

    def parse_string(self, params: str):
        validate_string(params, "params")
        tokens = shlex.split(params)
        self.parse_params(tokens)

    def parse_params(self, params: List[str]) -> None:
        """Выполняет парсинг строковых токенов в параметры
        команды и их значения"""
        pass

    def validate(self) -> None:
        """Выполняет проверку инициализированной команды
        на корректность заполненных параметров"""

        # Стадия #1. Проверяем соответствие типов параметров
        mandatory_params_count = 0
        for idx, param in enumerate(self.params_schema):
            if idx > len(self.params_values) - 1:
                # Значений оказалось меньше, чем параметров.
                # Это допустимо для необязательных параметров.
                break

            param_value = self.params_values[idx]
            if not param.check_type(param_value):
                raise DbCommandException(f"Параметр '{param.name}' не соответствует "
                                         f"целевому типу {param.type_ref}. "
                                         f"Фактический тип: {type(param_value)}")

            if param.is_mandatory:
                mandatory_params_count += 1

        # Стадия #2. Проверяем количество обязательных параметров.
        if mandatory_params_count > len(self.params_values):
            raise DbCommandException(f"Отличается минимальное ({mandatory_params_count}) "
                                     f"и фактическое ({len(self.params_values)}) количества "
                                     f"параметров команды ")

    def _get_number_of_values(self) -> int:
        """Получение количества фактических параметров команды"""
        return len(self.params_values)

    def _get_param_value(self, index:int) -> Any|None:
        """Безопасное получение параметра по индексу.
        Если индекс выходит за границы массива значений, то метод возвращает None"""
        if index < 0:
            raise ValueError("Индекс не может быть отрицательным")
        if index > self._get_number_of_values() - 1:
            return None
        return self.params_values[index]

    def execute(self) -> List[List[str]]:
        """Производит выполнение команды"""
        pass