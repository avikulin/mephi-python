from enum import StrEnum


class DbPredicateOperation (StrEnum):
    GT = ">"
    GE = ">="
    LT = "<"
    LE = "<="
    EQ = "="
    NEQ = "!="

    @classmethod
    def from_string(cls, value:str):
        cleaned_value = value.strip().lower()
        for po in DbPredicateOperation:
            if cleaned_value == po.value:
                return po
        raise ValueError(f"Unsupported operation: {value}")