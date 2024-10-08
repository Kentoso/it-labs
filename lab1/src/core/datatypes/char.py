from core.datatypes.datatype import DataType


class Char(DataType):
    def __init__(self, value: str):
        self.value = value
        if not self.validate():
            raise ValueError(f"Invalid char: {value}")

    def validate(self) -> bool:
        return isinstance(self.value, str) and len(self.value) == 1

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Char) and self.value == other.value

    def __repr__(self) -> str:
        return f"Char({self.value})"

    def __str__(self) -> str:
        return self.value

    def to_json_value(self):
        return self.value
