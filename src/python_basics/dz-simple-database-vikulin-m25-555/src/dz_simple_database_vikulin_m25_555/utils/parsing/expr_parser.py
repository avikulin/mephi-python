import re
from typing import List, Tuple

from dz_simple_database_vikulin_m25_555.command.base.db_command_base import (
    DbCommandException,
)
from dz_simple_database_vikulin_m25_555.command.expression.db_predicate_operation import DbPredicateOperation
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class ParseExprHelper:
    REGEX_BRACKETS_EXPR = re.compile("(?<=\\().+(?=\\))",
                                        re.IGNORECASE)

    REGEX_PARENTHESIS_CLEANER = re.compile("(?<=['\"])"
                                           "([^'\"\\s]+)"
                                           "(?=['\"])")
    JUST_ONE_PART = 1 # ожидается только 1 токен
    NUMBER_OF_ASSIGNMENT_PARTS = 2 # lvalue, rvalue
    NUMBER_OF_PREDICATE_PARTS = 3  # lvalue, operation, rvalue

    @classmethod
    def parse_brackets(cls, source: str,
                            description: str,
                            tokens_splitter:str|None = None) -> List[str]:
        """Из переданной строки вычленяет выражение в скобках
        и разбивает его на токены, если был передан разделитель."""

        err_msg = f"Нарушение семантики команды '{description}'"
        validate_string(source, err_msg)
        validate_string(description, err_msg)

        match = ParseExprHelper.REGEX_BRACKETS_EXPR.search(source)
        if match is None:
            raise DbCommandException(err_msg)

        values_token = match.group().strip()

        return values_token.split(tokens_splitter) \
                    if tokens_splitter is not None \
                        else [values_token]

    @classmethod
    def parse_predicate(cls, source: str,
                        prev_token:str,
                        next_token:str,
                        description: str) -> Tuple[str, str, str]:
        validate_string(source, 'source')
        validate_string(description, 'description')

        # Сортируем по длине операции: сначала '>=' и '<=',
        # а потом все остальные - тогда regexp будет работать правильно
        predicate_ops = "|".join(
            sorted(
                [op.value for op in DbPredicateOperation],
                key=len,
                reverse=True
            )
        )

        left = "^" if prev_token is None else f"(?<={prev_token}\\s)"
        right = "$" if next_token is None else f"(?=\\s{next_token})"
        pattern = (f"{left}"
                   f"(\\w+)\\s*({predicate_ops})\\s*(.+)"
                   f"{right}")

        match = re.search(pattern, source, re.IGNORECASE)
        if (match is None or
            len(match.groups()) != ParseExprHelper.NUMBER_OF_PREDICATE_PARTS):
            err_msg = f"Нарушение семантики команды '{description}'"
            raise DbCommandException(err_msg)
        return (match.group(1).strip(),
                match.group(2).strip(),
                ParseExprHelper.clear_parenthesis(
                    match.group(3).strip(),
                    description)
                )

    @classmethod
    def parse_assignment(cls, source: str,
                         prev_token: str,
                         next_token: str,
                         description: str) -> Tuple[str, str]:
        validate_string(source, 'source')
        validate_string(description, 'description')

        left = "^" if prev_token is None else f"(?<={prev_token}\\s)"
        right = "$" if next_token is None else f"(?=\\s{next_token})"
        pattern = (f"{left}"
                   f"(\\w+)\\s*=\\s*(.+)"
                   f"{right}")

        match = re.search(pattern, source, re.IGNORECASE)
        if (match is None or
                len(match.groups()) != ParseExprHelper.NUMBER_OF_ASSIGNMENT_PARTS):
            err_msg = f"Нарушение семантики команды '{description}'"
            raise DbCommandException(err_msg)
        return (match.group(1),
                ParseExprHelper.clear_parenthesis(match.group(2), description))

    @classmethod
    def clear_parenthesis(cls, source:str, description: str) -> str:
        err_msg = f"Нарушение семантики команды '{description}'"
        validate_string(source, err_msg)
        validate_string(description, err_msg)

        match = ParseExprHelper.REGEX_PARENTHESIS_CLEANER.search(source)
        if (match is None or
            len(match.groups()) != ParseExprHelper.JUST_ONE_PART):
            # если кавычек не нашли - возвращаем исходный вариант
            return source
        return match.group()