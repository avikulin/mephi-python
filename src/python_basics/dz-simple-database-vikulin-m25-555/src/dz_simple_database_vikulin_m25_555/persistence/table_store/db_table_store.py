from pathlib import Path
from typing import List

from dz_simple_database_vikulin_m25_555.config.db_config import DbConfig, MAX_ROWS_SELECT
from dz_simple_database_vikulin_m25_555.command.expression.db_predicate import DbPredicate
from dz_simple_database_vikulin_m25_555.command.expression.db_predicate_operation import DbPredicateOperation
from dz_simple_database_vikulin_m25_555.utils.io import read_json, write_json
from dz_simple_database_vikulin_m25_555.model.db_datatype import DbDataType
from dz_simple_database_vikulin_m25_555.model.db_table import DbTable, PKEY_NAME
from dz_simple_database_vikulin_m25_555.persistence.table_store.db_value_constructor import DbValueConstructor
from dz_simple_database_vikulin_m25_555.utils.io.json_io import touch_file
from dz_simple_database_vikulin_m25_555.utils.validation import validate_string, validate_list



class DbOperationException(Exception):
    """Доменное исключение для обработки ошибок в параметрах операций"""

class DbSchemaException(Exception):
    """Доменное исключение для обработки ошибок несоответствия схемы данных"""

class DbTableStore:
    def __init__(self, schema: DbTable, data_file_name:Path, config:DbConfig):
        if schema is None:
            raise ValueError(
                f"Ошибка инициализации параметров: "
                f"отсутствует параметр 'schema'"
            )

        if data_file_name is None:
            raise ValueError(
                f"Ошибка инициализации параметров: "
                f"отсутствует параметр 'data_file_name'"
            )
        if config is None:
            raise DbOperationException(
                f"Ошибка инициализации параметров: "
                f"отсутствует параметр 'config'")
        self.schema = schema
        self.table_name = schema.name
        self.data_file_name = data_file_name
        self.config = config

        self.column_names = []
        self.column_types = []
        for column in self.schema.columns[1:]:
            self.column_names.append(column.name)
            self.column_types.append(column.datatype)

        # загрузить типизированную информацию в арену
        self.arena = {} # key = ID, value = List[Any]
        self._ensure_data_layout()



    def _ensure_data_layout(self):
        """Готовит файл данных кортежей: создаёт при отсутствии,
        читает содержимое в self.arena."""
        if not self.data_file_name.exists():
            touch_file(self.data_file_name) # создаем, если его нет
            write_json(self.data_file_name, {})

        raw_data = read_json(self.data_file_name)

        for pkey, row_values_str in raw_data.items():
            if len(row_values_str) != len(self.column_types):
                raise DbSchemaException(f"Строка #{pkey} не соответствует "
                                 f"схеме таблицы '{self.schema.name}'")
            row_typed_values = []
            for index, column_value_str in enumerate(row_values_str):
                data_type:DbDataType = self.column_types[index]
                column_typed_value = DbValueConstructor.construct(column_value_str, data_type)
                row_typed_values.append(column_typed_value)

            typed_pkey = DbValueConstructor.construct(pkey, DbDataType.INTEGER)
            self.arena[typed_pkey] = row_typed_values


    def flush(self):
        """Выполнение записи оперативного буфера на диск"""
        write_json(self.data_file_name, self.arena)

    def select_tuples(self, predicate: DbPredicate = None) -> List[List[str]]:
        # если ищем по строгому соответствию 'ID' - то используем индекс
        if (predicate is not None and
                predicate.column.name == PKEY_NAME and
                    predicate.operation == DbPredicateOperation.EQ):
            pkey = predicate.value
            row_values = self.arena.get(pkey,[])
            if len(row_values) == 0:
                return []

            result = [str(pkey)]
            result.extend(row_values)
            return [result] # по умолчанию

        column_index = None
        if predicate is not None:
            column_index = self.column_names.index(predicate.column.name) \
                                if predicate.column.name != PKEY_NAME \
                                    else -1
        result = []
        result_rows_count = 0
        result_rows_limit = self.config.data[MAX_ROWS_SELECT]
        for row_pkey, row_data in self.arena.items():
            value_to_check = None
            if column_index is not None:
                value_to_check = row_pkey if column_index == -1 \
                                        else row_data[column_index]
            # если предикат не задан - выводим все строки в пределах лимита
            if predicate is None or predicate.apply(value_to_check):
                result_item = [str(row_pkey)]
                result_item.extend([str(value) for value in row_data])
                result.append(result_item)

                # контролируем объем выдачи
                result_rows_count += 1
                if result_rows_count == result_rows_limit:
                    break

        return result

    def insert_tuple(self, data: List[str]) -> List[List[str]]:
        validate_list(data, "data")
        row_pkey = int(data[0])
        if row_pkey in self.arena.keys():
            raise DbOperationException(f"Первичный ключ {row_pkey} уже существует к таблице")

        row_values = []
        for index, str_value in enumerate(data[1:]):
            datatype = self.column_types[index]
            typed_value = DbValueConstructor.construct(str_value, datatype)
            row_values.append(typed_value)

        self.arena[row_pkey] = row_values

        # возвращаем вставленную строку
        result = [str(row_pkey)]
        result.extend(row_values)

        # сохраняем изменения на диск
        self.flush()

        # возвращаем вставленные строки
        return [result]

    def delete_tuple(self, predicate: DbPredicate) -> List[List[str]]:
        tuples_to_delete = self.select_tuples(predicate)
        if len(tuples_to_delete) == 0:
            return []

        for index in range(len(tuples_to_delete)):
            tuple_to_delete = tuples_to_delete[index]
            id_to_delete = int(tuple_to_delete[0])
            self.arena.pop(id_to_delete)

        # сохраняем изменения на диск
        self.flush()

        # возвращаем удаленные строки
        return tuples_to_delete

    def update_tuple(self, column_name:str, value: str, predicate: DbPredicate) -> List[List[str]]:
        validate_string(column_name, "column_name")
        validate_string(value, "value")

        # ID не учитываем, так как его обновлять нельзя
        if column_name == PKEY_NAME:
            raise DbOperationException(f"Запрещено обновлять значение "
                                       f"первичного ключа записи ({PKEY_NAME})")

        if column_name not in self.column_names:
            raise DbOperationException(f"Поле {column_name} не входит "
                                       f"в схему таблицы '{self.table_name}: "
                                       f"{self.column_names}'")
        if predicate is None:
            raise DbOperationException("Не задано условие обновления строк")

        tuples_for_update = self.select_tuples(predicate)
        if len(tuples_for_update) == 0:
            return []

        update_column_index = self.column_names.index(column_name)
        update_column_type = self.column_types[update_column_index]
        filter_column_name = predicate.column.name
        filter_column_index = -1 if filter_column_name == PKEY_NAME \
                                 else self.column_names.index(filter_column_name)

        for index in range(len(tuples_for_update)):
            tuple_to_update = tuples_for_update[index]
            filter_str_value = tuple_to_update[1 + filter_column_index]
            filter_column_type = predicate.column.datatype
            filter_typed_value = DbValueConstructor.construct(filter_str_value,
                                                              filter_column_type)
            if predicate.apply(filter_typed_value):
                tuple_to_update[1+ update_column_index] = str(value)
                id_to_update = int(tuple_to_update[0])
                new_typed_value = DbValueConstructor.construct(value,
                                                               update_column_type)
                self.arena[id_to_update][update_column_index] = new_typed_value

        # сохраняем изменения на диск
        self.flush()

        # возвращаем измененные строки
        return tuples_for_update