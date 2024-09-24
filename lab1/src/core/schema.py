from enum import Enum
from datatypes.money import Money, MoneyInterval


class DataType(str, Enum):
    INTEGER = "integer"
    REAL = "real"
    CHAR = "char"
    STRING = "string"
    MONEY = "money"
    MONEY_INTERVAL = "money_interval"


class Schema:
    def __init__(self, fields: dict):
        self.fields: dict = fields

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Schema):
            return False

        number_of_keys_equal = len(self.fields.keys()) == len(other.fields.keys())
        if not number_of_keys_equal:
            return False

        are_keys_equal = set(self.fields.keys()) == set(other.fields.keys())
        if not are_keys_equal:
            return False

        are_all_types_equal = all(
            [self.fields[key] == other.fields[key] for key in self.fields.keys()]
        )
        if not are_all_types_equal:
            return False

        return True

    def _validate_field(self, field: str, value):
        field_type = self.fields[field]
        print(field_type, value, type(value))

        if field_type == DataType.INTEGER:
            return isinstance(value, int) and value >= -(2**31) and value <= 2**31 - 1

        if field_type == DataType.REAL:
            return isinstance(value, float)

        if field_type == DataType.CHAR:
            return isinstance(value, str) and len(value) == 1

        if field_type == DataType.STRING:
            print(value, type(value))
            return isinstance(value, str)

        if field_type == DataType.MONEY:
            # (isinstance(value, str) and Money.parse(value)) or
            return isinstance(value, Money)

        if field_type == DataType.MONEY_INTERVAL:
            return isinstance(value, MoneyInterval)

    def validate(self, row: dict):
        for field, value in row.items():
            if field not in self.fields:
                return False, f"Unknown field: {field}"

            if not self._validate_field(field, value):
                return False, f"Invalid value for field `{field}`: {value}"

        return True, None
