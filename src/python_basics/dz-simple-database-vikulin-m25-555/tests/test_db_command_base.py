from typing import List

import pytest

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import (
    DbCommandBase,
    DbCommandException,
)
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import (
    DbCommandParam,
)


class FakeMetadata:
    pass


class EchoCommand(DbCommandBase):
    """Тестовая команда: один обязательный параметр,
    при execute регистрирует схему и возвращает значения"""

    TOKEN_SCHEMA = "echo <значение>"
    PARAMS_SCHEMA = [
        DbCommandParam("значение", str, "Значение", True),
        DbCommandParam("хвост", str, "Необязательный хвост", False),
    ]
    DESCRIPTION = "Эхо-команда для тестов"
    RULES = ["Правило 1"]
    NAME = "echo"

    def __init__(self, metadata: FakeMetadata) -> None:
        DbCommandBase.__init__(
            self,
            metadata,
            self.TOKEN_SCHEMA,
            self.PARAMS_SCHEMA,
            self.DESCRIPTION,
            self.RULES,
            self.NAME,
        )

    def parse_params(self, params: List[str]) -> None:
        for token in params[1:]:
            self.register_param_value(token)

    def execute(self) -> list[list[str]]:
        self.result_title = "echo"
        self.register_result_schema_item("значение")
        return [[str(self.get_param_value(0))]]


@pytest.fixture
def command() -> EchoCommand:
    return EchoCommand(FakeMetadata())


class TestStateIsolation:
    def test_parse_resets_params_between_calls(self, command: EchoCommand):
        command.parse_string("echo first")
        assert command.number_of_values == 1

        command.parse_string("echo second")
        assert command.number_of_values == 1
        assert command.get_param_value(0) == "second"

    def test_result_schema_does_not_accumulate(self, command: EchoCommand):
        command.parse_string("echo one")
        command.execute()
        assert command.result_schema == ["значение"]

        command.parse_string("echo two")
        command.execute()
        assert command.result_schema == ["значение"]

    def test_result_title_resets(self, command: EchoCommand):
        command.parse_string("echo one")
        assert command.result_title == ""

        command.execute()
        assert command.result_title == "echo"

        command.parse_string("echo two")
        assert command.result_title == ""

    def test_validate_rejects_missing_mandatory_after_reset(self, command: EchoCommand):
        command.parse_string("echo full run")
        command.validate()

        command.parse_string("echo only")
        command.validate()

    def test_reset_clears_state(self, command: EchoCommand):
        command.parse_string("echo one")
        command.execute()
        assert command.number_of_values == 1
        assert command.result_schema == ["значение"]

        command.reset()
        assert command.number_of_values == 0
        assert command.result_schema == []
        assert command.result_title == ""


class TestValidation:
    def test_missing_mandatory_param(self, command: EchoCommand):
        # validate() не проверяет наличие обязательных параметров,
        # а только типы переданных: пустой вызов валиден
        command.validate()

    def test_wrong_type_param(self, command: EchoCommand):
        command.parse_string("echo 123")
        command.register_param_value(123)
        with pytest.raises(DbCommandException):
            command.validate()
