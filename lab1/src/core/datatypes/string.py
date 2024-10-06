from core.datatypes.datatype import DataType


class String(DataType):
    def __init__(self, value: str):
        self.value = value
        if not self.validate():
            raise ValueError(f"Invalid string: {value}")

    def validate(self) -> bool:
        return isinstance(self.value, str)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, String) and self.value == other.value

    def __repr__(self) -> str:
        return f"String({self.value})"
