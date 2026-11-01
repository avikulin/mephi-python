from datetime import UTC, datetime

import pytest

from dz_simple_database_vikulin_m25_555.model.db_datatype import DbDataType


class TestFromString:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("string", DbDataType.STRING),
            ("integer", DbDataType.INTEGER),
            ("float", DbDataType.FLOAT),
            ("datetime", DbDataType.DATETIME),
            ("  INTEGER  ", DbDataType.INTEGER),
            ("Float", DbDataType.FLOAT),
        ],
    )
    def test_valid_names(self, raw: str, expected: DbDataType):
        assert DbDataType.from_string(raw) is expected

    @pytest.mark.parametrize("raw", ["unknown", "", "int", "str", "123"])
    def test_invalid_names(self, raw: str):
        with pytest.raises(ValueError, match="Unsupported datatype"):
            DbDataType.from_string(raw)


class TestValidate:
    def test_string_accepts_any_value(self, datatype_string: DbDataType):
        assert datatype_string.validate("")
        assert datatype_string.validate("abc")
        assert datatype_string.validate("42")

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("42", True),
            ("-42", True),
            ("+42", True),
            ("0", True),
            ("42.5", False),
            ("abc", False),
            ("", False),
            ("12a", False),
        ],
    )
    def test_integer(self, datatype_integer: DbDataType, value: str, expected: bool):
        assert datatype_integer.validate(value) is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("42.5", True),
            ("-0.5", True),
            (".5", True),
            ("1e3", True),
            ("42", True),
            ("abc", False),
            ("", False),
        ],
    )
    def test_float(self, value: str, expected: bool):
        assert DbDataType.FLOAT.validate(value) is expected

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            (datetime.now(UTC).isoformat(), True),
            ("2026-10-31T15:45:30", True),
            ("2026-10-31T15:45:30+03:00", True),
            ("2026-10-31", True),
            ("not a date", False),
            ("", False),
            ("31.10.2026", False),
        ],
    )
    def test_datetime(self, value: str, expected: bool):
        assert DbDataType.DATETIME.validate(value) is expected
