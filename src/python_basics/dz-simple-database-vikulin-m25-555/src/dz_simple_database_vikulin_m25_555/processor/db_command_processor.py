import re
import shlex
from enum import StrEnum

import prompt
from prettytable import PrettyTable

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import (
    DbCommandBase,
)
from dz_simple_database_vikulin_m25_555.command.factory.db_command_factory import (
    DbCommandFactory,
)
from dz_simple_database_vikulin_m25_555.utils.console.db_console_colors import Color
from dz_simple_database_vikulin_m25_555.utils.console.db_console_primitives import (
    Primitive,
)
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbRuntimeException(Exception):
    """"Доменное исключение для обработки проблем в Runtime"""
    pass

class CommandType(StrEnum):
    EXIT = "exit"
    HELP = "help"
    DB_CMD = "database command"


class DbCommandProcessor:
    CMD_HELP = "help"
    CMD_EXIT = "exit"

    def __init__(self, cmd_factory: DbCommandFactory):
        if cmd_factory is None:
            raise DbRuntimeException("Невозможно инициализировать: "
                                     "передана пустая ссылка на "
                                     "фабрику команд")
        self.cmd_factory = cmd_factory
        self.cmd_names = cmd_factory.all_command_names
        self.re_help = re.compile(f"^{DbCommandProcessor.CMD_HELP}(.+)?$",
                                  re.IGNORECASE)


    def hava_to_exit(self, prompt: str) -> bool:
        """Выполняет проверку на введенную комманду EXIT"""
        validate_string(prompt, "prompt")
        tokens = shlex.split(prompt)
        return (len(tokens) == 1 and
                tokens[0] == DbCommandProcessor.CMD_EXIT)

    def need_help(self, prompt) -> bool:
        validate_string(prompt, "prompt")
        match: re.Match[str]|None = self.re_help.match(prompt)
        return bool(match)

    def help_list_of_commands(self) ->str:
        """Выводит справку по поддерживаемым командам БД"""
        table = PrettyTable(["Команда"])
        for cmd in self.cmd_factory.all_commands:
            table.add_row([cmd.name])
        return (f""
                f"{Primitive.OUTPUT}Система поддерживает следующий набор команд:\n"
                f"{table}"
                f"\n"
                f"Для получения подробной справки введите:\n"
                f"{Color.OKCYAN}help <имя команды>{Color.ENDC}\n")

    def help_concrete_command(self, cmd_name:str) ->str:
        """Выводит справку по конкретной команде БД"""
        validate_string(cmd_name, "cmd_name")
        if cmd_name not in self.cmd_names:
            raise DbRuntimeException(f"Неизвестная команда: {cmd_name}")

        cmd = self.cmd_factory.get_command(cmd_name)

        return (f"{Primitive.HINT}Справка по встроенной функции "
                f"{Color.BOLD}{cmd_name}{Color.ENDC}:\n"
                f"{cmd.get_help()}\n"
                f"{Primitive.END_HINT}")

    def process_help(self, prompt:str) -> str:
        """Обрабатывает запрос на справку (запрос начинается с 'HELP')"""
        validate_string(prompt, "prompt")
        tokens = shlex.split(prompt)
        if tokens[0] != DbCommandProcessor.CMD_HELP:
            raise DbRuntimeException(f"Ошибка роутинга команды: {prompt}")

        if len(tokens) == 1:
            return self.help_list_of_commands()

        cmd_name = " ".join(tokens[1:])
        return self.help_concrete_command(cmd_name)


    def process_command(self, prompt:str, cmd: DbCommandBase) -> str:
        if cmd is None:
            raise DbRuntimeException("Передана пустая ссылка на команду")
        validate_string(prompt, "prompt")
        cmd.parse_string(prompt)
        cmd.validate()
        result = cmd.execute()
        schema = cmd.result_schema
        table = PrettyTable(schema)
        for row in result:
            table.add_row(row)

        return (f"{Primitive.OUTPUT}{cmd.result_title}:\n"
                f"{table}")

    def query_prompt(self)->str:
        style = f"{Primitive.INPUT}{Color.HEADER}{Color.BOLD}"
        prompt.PROMPT = style
        return prompt.string(style).strip()

    def process_prompt(self, prompt: str):
        validate_string(prompt, "prompt")
        cleaned_prompt = prompt.strip()

        if self.hava_to_exit(cleaned_prompt):
            print(f"{Primitive.LOG}Выход из программы")
            return False

        if self.need_help(cleaned_prompt):
            print(self.process_help(cleaned_prompt))
            return True

        cmd = self.cmd_factory.get_command(cleaned_prompt)
        print(self.process_command(cleaned_prompt, cmd))
        return True

    def run(self):
        to_be_continued = True
        while to_be_continued:
            user_prompt = self.query_prompt()
            to_be_continued = self.process_prompt(user_prompt)