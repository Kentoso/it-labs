import core.datatypes as datatypes
from enum import Enum


class DataTypeNames(str, Enum):
    INTEGER = "integer"
    REAL = "real"
    CHAR = "char"
    STRING = "string"
    MONEY = "money"
    MONEY_INTERVAL = "money_interval"


name_to_datatype = {
    DataTypeNames.INTEGER: datatypes.Integer,
    DataTypeNames.REAL: datatypes.Real,
    DataTypeNames.CHAR: datatypes.Char,
    DataTypeNames.STRING: datatypes.String,
    DataTypeNames.MONEY: datatypes.Money,
    DataTypeNames.MONEY_INTERVAL: datatypes.MoneyInterval,
}


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

    def validate(self, row: dict):
        result = {}
        for field, value in row.items():
            if field not in self.fields:
                return False, f"Unknown field: {field}"

            field_type = self.fields[field]

            field_type = name_to_datatype[field_type]

            try:
                field_value = field_type(value)
                result[field] = field_value
            except ValueError as e:
                return None, f"Invalid field {field}: {str(e)}"

        return result, None
