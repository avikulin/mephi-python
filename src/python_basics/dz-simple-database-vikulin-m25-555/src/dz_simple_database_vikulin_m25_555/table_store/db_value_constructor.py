from datetime import datetime
from typing import Union

from dz_simple_database_vikulin_m25_555.model.db_datatype import DbDataType


class DbValueConstructor:
    @classmethod
    def construct(
        cls, source: str, datatype: DbDataType
    ) -> Union[str, bool, int, float, datetime]:
        clean_value = source.strip()
        match datatype:
            case DbDataType.STRING:
                return clean_value
            case DbDataType.BOOLEAN:
                invariant_str = clean_value.lower()
                return True if invariant_str == "true" else False
            case DbDataType.INTEGER:
                return int(clean_value)
            case DbDataType.FLOAT:
                return float(clean_value)
            case DbDataType.DATETIME:
                return datetime.fromisoformat(source)
