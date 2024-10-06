import pytest
from schema import Schema, DataTypeNames
from datatypes.money import Money, MoneyInterval


@pytest.fixture
def sample_schema():
    return Schema(
        {
            "id": DataTypeNames.INTEGER,
            "price": DataTypeNames.MONEY,
            "description": DataTypeNames.STRING,
            "rating": DataTypeNames.REAL,
            "currency_code": DataTypeNames.CHAR,
            "price_range": DataTypeNames.MONEY_INTERVAL,
        }
    )


def test_validate_unknown_field(sample_schema: Schema):
    row = {"unknown_field": "some_value"}
    ok, reason = sample_schema.validate(row)
    assert not ok
    assert "Unknown field: unknown_field" in reason


def test_validate_valid_row(sample_schema: Schema):
    row = {
        "id": 123,
        "price": "50 USD",
        "description": "A great product",
        "rating": 4.8,
        "currency_code": "U",
        "price_range": "40 USD - 60 USD",
    }
    ok, reason = sample_schema.validate(row)
    assert ok
    assert reason is None


def test_validate_invalid_row(sample_schema: Schema):
    row = {
        "id": "invalid_id",  # invalid integer
        "price": "50 USD",
        "description": "A great product",
        "rating": 4.8,
        "currency_code": "USD",  # invalid CHAR, length > 1
        "price_range": "40 USD - 60 USD",
    }
    ok, reason = sample_schema.validate(row)
    assert not ok
    assert "Invalid field id" in reason or "Invalid field currency_code" in reason
