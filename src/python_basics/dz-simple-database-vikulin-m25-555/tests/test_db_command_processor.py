import pytest

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import (
    DbCommandBase,
)
from dz_simple_database_vikulin_m25_555.command.base.db_command_param import (
    DbCommandParam,
)
from dz_simple_database_vikulin_m25_555.command.factory.db_command_factory import (
    DbCommandFactory,
)
from dz_simple_database_vikulin_m25_555.processor.db_command_processor import (
    DbCommandProcessor,
)


class FakeMetadata:
    pass


class SelectStub(DbCommandBase):
    """Стуб селекта: имитирует накопление result_schema в execute"""

    TOKEN_SCHEMA = "select from <имя_таблицы>"
    PARAMS_SCHEMA = [DbCommandParam("имя", str, "Имя таблицы", True)]
    DESCRIPTION = "стуб"
    RULES = ["стуб-правило"]
    NAME = "select"

    def __init__(self, metadata) -> None:
        DbCommandBase.__init__(
            self, metadata, self.TOKEN_SCHEMA, self.PARAMS_SCHEMA,
            self.DESCRIPTION, self.RULES, self.NAME,
        )
        self.table_names = ["ID"]

    def parse_params(self, params) -> None:
        self.register_param_value("stub-table")

    def execute(self) -> list[list[str]]:
        self.result_title = "Из таблицы получены строки"
        for name in self.table_names:
            self.register_result_schema_item(name)
        return [["1"]]


@pytest.fixture
def processor() -> DbCommandProcessor:
    factory = DbCommandFactory()
    factory.register_command(r"^select\s+from\s+\w+$", SelectStub(FakeMetadata()))
    return DbCommandProcessor(factory)


class TestRepeatedSelect:
    def test_field_names_unique_across_calls(self, processor: DbCommandProcessor):
        cmd = processor.cmd_factory.get_command("select from books")

        first = processor.process_command("select from books", cmd)
        assert "ID" in first

        # второй вызов той же команды-одиночки:
        # result_schema не должна задвоиться
        second = processor.process_command("select from books", cmd)
        assert "ID" in second
        assert second.count("ID") == 1  # нет дублей в заголовке таблицы
