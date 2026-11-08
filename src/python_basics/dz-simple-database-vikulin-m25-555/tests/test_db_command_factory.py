import pytest

from dz_simple_database_vikulin_m25_555.command.factory.db_command_factory import (
    DbCommandException,
    DbCommandFactory,
)


class SimpleCmd:
    NAME = "simple"

    def __init__(self):
        self.calls = 0


class TestFactoryReturnsSameInstance:
    def test_get_command_returns_registered_instance(self):
        factory = DbCommandFactory()
        cmd = SimpleCmd()
        factory.register_command(r"^simple$", cmd)
        assert factory.get_command("simple") is cmd

    def test_same_instance_returned_repeatedly(self):
        """Команда-singleton: state команды переживает вызовы,
        поэтому команда обязана сбрасывать per-invocation state."""
        factory = DbCommandFactory()
        cmd = SimpleCmd()
        factory.register_command(r"^simple$", cmd)

        first = factory.get_command("simple")
        second = factory.get_command("simple")
        assert first is second

    def test_unknown_pattern_raises(self):
        factory = DbCommandFactory()
        with pytest.raises(DbCommandException, match="Не найдено подходящего шаблона"):
            factory.get_command("unknown")
