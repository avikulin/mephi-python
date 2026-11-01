import pytest

from dz_simple_database_vikulin_m25_555.model.db_column import DbColumn
from dz_simple_database_vikulin_m25_555.model.db_datatype import DbDataType
from dz_simple_database_vikulin_m25_555.model.db_table import PKEY_NAME, DbTable


@pytest.fixture
def datatype_string() -> DbDataType:
    return DbDataType.STRING


@pytest.fixture
def datatype_integer() -> DbDataType:
    return DbDataType.INTEGER


@pytest.fixture
def column_name() -> DbColumn:
    return DbColumn("name", DbDataType.STRING, is_mandatory=True, is_primary=False)


@pytest.fixture
def column_age() -> DbColumn:
    return DbColumn("age", DbDataType.INTEGER, is_mandatory=False, is_primary=False)


@pytest.fixture
def column_pkey() -> DbColumn:
    return DbColumn(PKEY_NAME, DbDataType.INTEGER, is_mandatory=True, is_primary=True)


@pytest.fixture
def schema() -> dict[str, str]:
    return {"name": "string", "age": "integer", "born": "datetime"}


@pytest.fixture
def table(schema: dict[str, str]) -> DbTable:
    return DbTable.from_schema("people", schema)


@pytest.fixture
def table_json(table: DbTable) -> str:
    return table.to_json()


@pytest.fixture
def column_json(column_name: DbColumn) -> str:
    return column_name.to_json()
