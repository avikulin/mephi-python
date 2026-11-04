from typing import Tuple

from dz_simple_database_vikulin_m25_555.expression.db_predicate import DbPredicate
from dz_simple_database_vikulin_m25_555.expression.db_predicate_operation import DbPredicateOperation, \
    DbPredicateOperationException
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable
from dz_simple_database_vikulin_m25_555.table_store.db_value_constructor import DbValueConstructor
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string


class DbPredicateFactory:
    @classmethod
    def process_predicate(cls, source:str, table: DbTable) -> DbPredicate:
        """Создает объект DbPredicate из строкового представления"""
        validate_string(source, "source")
        lvalue, op, rvalue = DbPredicateFactory.find_and_split(source)
        column = table.get_column(lvalue)
        data_type = column.datatype
        typed_criteria = DbValueConstructor.construct(rvalue, data_type)
        return DbPredicate(column, op, typed_criteria)

    @classmethod
    def find_and_split(cls, value:str) -> Tuple[str, DbPredicateOperation, str]:
        validate_string(value, "source")
        cleaned_value = value.strip().replace(" ","").lower()
        results = {}
        # Ищем все вхождения.
        # Вхождения могут пересекаться: например '>' и '>=' и '='
        for po in DbPredicateOperation:
            index = str.find(cleaned_value, po)
            if index == -1:
                continue
            if index == 0 or index == len(cleaned_value) - 1:
                raise DbPredicateOperationException(f"Неправильный формат предиката: {value}")
            results[po] = index

        # контролируем, что вхождения есть
        if len(results) == 0:
            raise DbPredicateOperationException(
                f"Выражение не является предикатом: '{value}'"
            )

        #отбираем результирующее вхождение:
        # - находится в самой левой позиции
        # - имеет максимальную длину вхождения

        result_index:int = -1
        result_operation:DbPredicateOperation = None
        for operation, index in results.items():
            if result_operation is None:
                result_operation = DbPredicateOperation.from_string(operation)
                result_index = index
                continue # приоритет 0

            if result_index > index:
                result_operation = DbPredicateOperation.from_string(operation)
                result_index = index
                continue # приоритет 1

            # приоритет 2
            if len(result_operation) < len(operation):
                result_operation = DbPredicateOperation.from_string(operation)
                result_index = index


        lvalue = cleaned_value[:result_index]
        rvalue = cleaned_value[result_index+len(result_operation):]
        return lvalue, result_operation, rvalue
