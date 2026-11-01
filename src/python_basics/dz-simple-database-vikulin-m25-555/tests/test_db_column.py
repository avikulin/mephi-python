import dataclasses
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


class TestInit:
    def test_creates_with_all_fields(self, column_name: DbColumn):
        assert column_name.name == "name"
        assert column_name.datatype is DbDataType.STRING
        assert column_name.is_mandatory is True
        assert column_name.is_primary is False

    def test_frozen(self, column_name: DbColumn):
        with pytest.raises(dataclasses.FrozenInstanceError):
            column_name.name = "other"


class TestValidateValue:
    def test_delegates_to_datatype(self, column_age: DbColumn):
        assert column_age.validate_value("42") is True
        assert column_age.validate_value("abc") is False


class TestToJson:
    def test_contains_all_fields(self, column_json: str):
        data = json.loads(column_json)
        assert data == {
            COLUMN_NAME: "name",
            DATATYPE_NAME: "string",
            IS_MANDATORY_NAME: True,
            IS_PRIMARY_NAME: False,
        }


class TestFromJson:
    def test_roundtrip(self, column_name: DbColumn, column_json: str):
        assert DbColumn.from_json(column_json) == column_name

    def test_invalid_json(self):
        with pytest.raises(ValueError, match="корректным JSON"):
            DbColumn.from_json("not json")

    def test_root_not_dict(self):
        with pytest.raises(TypeError, match="словарём"):
            DbColumn.from_json('["array"]')

    def _source(self, **overrides) -> str:
        data = {
            COLUMN_NAME: "name",
            DATATYPE_NAME: "string",
            IS_MANDATORY_NAME: True,
            IS_PRIMARY_NAME: False,
        }
        data.update(overrides)
        return json.dumps(data)

    def test_missing_name(self):
        source = self._source(**{COLUMN_NAME: None})
        with pytest.raises(ValueError, match=f"data\\['{COLUMN_NAME}'\\]"):
            DbColumn.from_json(source)

    def test_missing_datatype(self):
        source = self._source(**{DATATYPE_NAME: None})
        with pytest.raises(ValueError, match=f"data\\['{DATATYPE_NAME}'\\]"):
            DbColumn.from_json(source)

    def test_unknown_datatype(self):
        source = self._source(**{DATATYPE_NAME: "unknown"})
        with pytest.raises(ValueError, match="Unsupported datatype"):
            DbColumn.from_json(source)

    @pytest.mark.parametrize("flag", [IS_MANDATORY_NAME, IS_PRIMARY_NAME])
    def test_flags_must_be_bool(self, flag: str):
        source = self._source(**{flag: "yes"})
        with pytest.raises(TypeError, match="булевым"):
            DbColumn.from_json(source)

    def test_missing_flags(self):
        data = {
            COLUMN_NAME: "name",
            DATATYPE_NAME: "string",
        }
        with pytest.raises(TypeError, match="булевым"):
            DbColumn.from_json(json.dumps(data))
