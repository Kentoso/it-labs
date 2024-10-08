from core.datatypes.datatype import DataType


class Real(DataType):
    def __init__(self, value: float):
        self.value = value
        if not self.validate():
            raise ValueError(f"Invalid real: {value}")

    def validate(self) -> bool:
        return isinstance(self.value, float)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Real) and self.value == other.value

    def __repr__(self) -> str:
        return f"Real({self.value})"

    def __str__(self) -> str:
        return str(self.value)

    def to_json_value(self):
        return self.value
