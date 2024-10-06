from datatypes.datatype import DataType


class Integer(DataType):
    def __init__(self, value: int):
        self.value = value
        if not self.validate():
            raise ValueError(f"Invalid integer: {value}")

    def validate(self) -> bool:
        return (
            isinstance(self.value, int)
            and self.value >= -(2**31)
            and self.value <= 2**31 - 1
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Integer) and self.value == other.value

    def __repr__(self) -> str:
        return f"Integer({self.value})"
