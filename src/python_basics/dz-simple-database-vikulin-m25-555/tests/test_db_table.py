import json

import pytest

from dz_simple_database_vikulin_m25_555.model.db_column import (
    COLUMN_NAME,
    DATATYPE_NAME,
    IS_MANDATORY_NAME,
    IS_PRIMARY_NAME,
    DbColumn,
)
from dz_simple_database_vikulin_m25_555.model.db_datatype import DbDataType
from dz_simple_database_vikulin_m25_555.model.db_table import (
    COLUMNS_NAME as COLUMNS_NAME_KEY,
)
from dz_simple_database_vikulin_m25_555.model.db_table import (
    PKEY_NAME,
    DbTable,
)
from dz_simple_database_vikulin_m25_555.model.db_table import (
    TABLE_NAME as TABLE_NAME_KEY,
)


def _col(name: str, datatype: str, is_mandatory: bool, is_primary: bool) -> dict:
    return {
        COLUMN_NAME: name,
        DATATYPE_NAME: datatype,
        IS_MANDATORY_NAME: is_mandatory,
        IS_PRIMARY_NAME: is_primary,
    }


class TestInit:
    def test_creates_pkey_automatically(self, column_name: DbColumn):
        table = DbTable("people", [column_name])
        assert table.pkey.name == PKEY_NAME
        assert table.pkey.is_primary is True
        assert table.pkey.is_mandatory is True

    def test_accepts_columns(self, column_name: DbColumn, column_age: DbColumn):
        table = DbTable("people", [column_name, column_age])
        assert table.column_names == [PKEY_NAME, "name", "age"]

    def test_empty_name(self):
        with pytest.raises(ValueError, match="'name'"):
            DbTable("  ", [])

    def test_rejects_primary_column(self, column_pkey: DbColumn):
        with pytest.raises(ValueError, match="primary"):
            DbTable("people", [column_pkey])

    def test_rejects_non_column_items(self):
        with pytest.raises(TypeError, match="DbColumn"):
            DbTable("people", ["oops"])

    def test_rejects_empty_columns(self):
        with pytest.raises(ValueError, match="'columns'"):
            DbTable.from_columns("people", [])


class TestFromSchema:
    def test_creates_columns_from_mapping(self, schema: dict[str, str]):
        table = DbTable.from_schema("people", schema)
        assert table.name == "people"
        assert table.column_names == [PKEY_NAME, "name", "age", "born"]
        datatypes = [c.datatype for c in table.columns if not c.is_primary]
        assert datatypes == [
            DbDataType.STRING,
            DbDataType.INTEGER,
            DbDataType.DATETIME,
        ]

    def test_column_flags_default_false(self, schema: dict[str, str]):
        table = DbTable.from_schema("people", schema)
        for column in table.columns:
            if not column.is_primary:
                assert column.is_mandatory is False
                assert column.is_primary is False

    def test_empty_schema(self):
        with pytest.raises(ValueError, match="'columns'"):
            DbTable.from_schema("people", {})

    def test_unknown_datatype(self):
        with pytest.raises(ValueError, match="Unsupported datatype"):
            DbTable.from_schema("people", {"name": "unknown"})

    def test_empty_name(self):
        with pytest.raises(ValueError, match="'name'"):
            DbTable.from_schema("", {"name": "string"})


class TestFromColumns:
    def test_same_as_init(self, column_name: DbColumn, column_age: DbColumn):
        table = DbTable.from_columns("people", [column_name, column_age])
        assert table.column_names == [PKEY_NAME, "name", "age"]


class TestProperties:
    def test_columns_returns_copy(self, table: DbTable):
        snapshot = table.columns
        snapshot.clear()
        assert table.column_names == [PKEY_NAME, "name", "age", "born"]


class TestMetadata:
    def test_structure(self, table: DbTable):
        metadata = table.metadata
        assert set(metadata.keys()) == {TABLE_NAME_KEY, COLUMNS_NAME_KEY}
        assert metadata[TABLE_NAME_KEY] == "people"

    def test_columns_are_dbcolumn_objects(self, table: DbTable):
        columns = table.metadata[COLUMNS_NAME_KEY]
        assert all(isinstance(c, DbColumn) for c in columns)
        assert columns[0].name == PKEY_NAME
        assert columns[1].name == "name"
        assert columns[1].datatype is DbDataType.STRING

    def test_columns_include_pkey(self, table: DbTable):
        names = [c.name for c in table.metadata[COLUMNS_NAME_KEY]]
        assert names[0] == PKEY_NAME
        assert names == table.column_names

    def test_metadata_is_snapshot(self, table: DbTable):
        metadata = table.metadata
        metadata[COLUMNS_NAME_KEY].clear()
        assert table.metadata[COLUMNS_NAME_KEY] != []


class TestToJson:
    def test_structure(self, table_json: str):
        data = json.loads(table_json)
        assert data[TABLE_NAME_KEY] == "people"
        assert data[COLUMNS_NAME_KEY] == [
            _col(PKEY_NAME, "integer", True, True),
            _col("name", "string", False, False),
            _col("age", "integer", False, False),
            _col("born", "datetime", False, False),
        ]

    def test_pkey_serialized(self, table_json: str):
        data = json.loads(table_json)
        names = [c[COLUMN_NAME] for c in data[COLUMNS_NAME_KEY]]
        assert names[0] == PKEY_NAME


class TestFromJson:
    def test_roundtrip(self, table: DbTable, table_json: str):
        restored = DbTable.from_json(table_json)
        assert restored.name == table.name
        assert restored.columns == table.columns

    def test_invalid_json(self):
        with pytest.raises(ValueError, match="корректным JSON"):
            DbTable.from_json("not json")

    def test_root_not_dict(self):
        with pytest.raises(TypeError, match="словарём"):
            DbTable.from_json('["array"]')

    def test_missing_name(self):
        source = json.dumps(
            {
                COLUMNS_NAME_KEY: [
                    _col(PKEY_NAME, "integer", True, True),
                    _col("n", "string", False, False),
                ]
            }
        )
        with pytest.raises(ValueError, match=f"data\\['{TABLE_NAME_KEY}'\\]"):
            DbTable.from_json(source)

    def test_missing_columns(self):
        source = json.dumps({TABLE_NAME_KEY: "people"})
        with pytest.raises(TypeError, match=f"data\\['{COLUMNS_NAME_KEY}'\\]"):
            DbTable.from_json(source)

    def test_columns_not_list(self):
        source = json.dumps({TABLE_NAME_KEY: "people", COLUMNS_NAME_KEY: {}})
        with pytest.raises(TypeError, match="списком"):
            DbTable.from_json(source)

    def test_empty_columns(self):
        source = json.dumps({TABLE_NAME_KEY: "people", COLUMNS_NAME_KEY: []})
        with pytest.raises(ValueError, match="хотя бы одну колонку"):
            DbTable.from_json(source)

    def test_column_not_dict(self):
        source = json.dumps({TABLE_NAME_KEY: "people", COLUMNS_NAME_KEY: ["oops"]})
        with pytest.raises(TypeError, match="словарём"):
            DbTable.from_json(source)

    def test_wrong_pkey(self):
        source = json.dumps(
            {
                TABLE_NAME_KEY: "people",
                COLUMNS_NAME_KEY: [
                    _col(PKEY_NAME, "string", False, True),
                    _col("name", "string", False, False),
                ],
            }
        )
        with pytest.raises(ValueError, match="Первичный ключ"):
            DbTable.from_json(source)

    def test_pkey_missing_in_json(self):
        source = json.dumps(
            {
                TABLE_NAME_KEY: "people",
                COLUMNS_NAME_KEY: [_col("name", "string", False, False)],
            }
        )
        with pytest.raises(ValueError, match="Первичный ключ"):
            DbTable.from_json(source)
