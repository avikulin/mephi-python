import json

import pytest

from dz_simple_database_vikulin_m25_555.io import JsonIOError, read_json, write_json


@pytest.fixture
def json_path(tmp_path):
    return tmp_path / "cfg" / "test.json"


class TestReadJson:
    def test_reads_valid_object(self, json_path):
        write_json(json_path, {"key": "value", "num": 42})
        assert read_json(json_path) == {"key": "value", "num": 42}

    def test_unicode_content(self, json_path):
        write_json(json_path, {"text": "привет мир"})
        assert read_json(json_path) == {"text": "привет мир"}

    def test_missing_file(self, tmp_path):
        with pytest.raises(JsonIOError, match="не найден"):
            read_json(tmp_path / "missing.json")

    def test_invalid_json(self, json_path):
        json_path.parent.mkdir(parents=True)
        json_path.write_text("not json", encoding="utf-8")
        with pytest.raises(JsonIOError, match="JSON-формата"):
            read_json(json_path)

    def test_root_is_array(self, json_path):
        json_path.parent.mkdir(parents=True)
        json_path.write_text('["array"]', encoding="utf-8")
        with pytest.raises(JsonIOError, match="JSON-объект"):
            read_json(json_path)

    def test_root_is_scalar(self, json_path):
        json_path.parent.mkdir(parents=True)
        json_path.write_text("42", encoding="utf-8")
        with pytest.raises(JsonIOError, match="JSON-объект"):
            read_json(json_path)

    def test_bad_encoding(self, json_path):
        json_path.parent.mkdir(parents=True)
        json_path.write_bytes(b"\xff\xfe\x00")
        with pytest.raises(JsonIOError, match="кодировки"):
            read_json(json_path)


class TestWriteJson:
    def test_creates_parent_dirs(self, json_path):
        write_json(json_path, {"a": 1})
        assert json_path.exists()

    def test_overwrites_existing(self, json_path):
        write_json(json_path, {"a": 1})
        write_json(json_path, {"b": 2})
        assert read_json(json_path) == {"b": 2}

    def test_readable_formatting(self, json_path):
        write_json(json_path, {"a": 1})
        content = json_path.read_text(encoding="utf-8")
        assert "\n" in content  # indent=2
        assert json.loads(content) == {"a": 1}

    def test_unserializable_data(self, json_path):
        with pytest.raises(JsonIOError, match="не сериализуются"):
            write_json(json_path, {"bad": object()})
