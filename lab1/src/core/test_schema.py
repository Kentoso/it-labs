import pytest
from schema import Schema, DataType
from datatypes.money import Money, MoneyInterval


@pytest.fixture
def sample_schema():
    return Schema(
        {
            "id": DataType.INTEGER,
            "price": DataType.MONEY,
            "description": DataType.STRING,
            "rating": DataType.REAL,
            "currency_code": DataType.CHAR,
            "price_range": DataType.MONEY_INTERVAL,
        }
    )


def test_validate_valid_integer(sample_schema: Schema):
    row = {"id": 12345}
    assert sample_schema._validate_field("id", row["id"]) is True


def test_validate_invalid_integer(sample_schema: Schema):
    row = {"id": "not_an_integer"}
    assert sample_schema._validate_field("id", row["id"]) is False


def test_validate_valid_real(sample_schema: Schema):
    row = {"rating": 4.5}
    assert sample_schema._validate_field("rating", row["rating"]) is True


def test_validate_invalid_real(sample_schema: Schema):
    row = {"rating": "not_a_float"}
    assert sample_schema._validate_field("rating", row["rating"]) is False


def test_validate_valid_char(sample_schema: Schema):
    row = {"currency_code": "A"}
    assert sample_schema._validate_field("currency_code", row["currency_code"]) is True


def test_validate_invalid_char_length(sample_schema: Schema):
    row = {"currency_code": "USD"}
    assert sample_schema._validate_field("currency_code", row["currency_code"]) is False


def test_validate_invalid_char_type(sample_schema: Schema):
    row = {"currency_code": 123}
    assert sample_schema._validate_field("currency_code", row["currency_code"]) is False


def test_validate_valid_string(sample_schema: Schema):
    row = {"description": "This is a valid string"}
    assert sample_schema._validate_field("description", row["description"]) is True


def test_validate_invalid_string(sample_schema: Schema):
    row = {"description": 1234}
    assert sample_schema._validate_field("description", row["description"]) is False


def test_validate_valid_money(sample_schema: Schema):
    row = {"price": Money.create(100, "USD")}
    assert sample_schema._validate_field("price", row["price"]) is True


def test_validate_invalid_money(sample_schema: Schema):
    row = {"price": "not_money"}
    assert sample_schema._validate_field("price", row["price"]) is False


def test_validate_valid_money_interval(sample_schema: Schema):
    row = {"price_range": MoneyInterval.create(100, 200, "USD")}
    assert sample_schema._validate_field("price_range", row["price_range"]) is True


def test_validate_invalid_money_interval(sample_schema: Schema):
    row = {"price_range": "invalid_interval"}
    assert sample_schema._validate_field("price_range", row["price_range"]) is False


def test_validate_unknown_field(sample_schema: Schema):
    row = {"unknown_field": "some_value"}
    ok, reason = sample_schema.validate(row)
    assert not ok
    assert "Unknown field: unknown_field" in reason


def test_validate_valid_row(sample_schema: Schema):
    row = {
        "id": 123,
        "price": Money.create(50, "USD"),
        "description": "A great product",
        "rating": 4.8,
        "currency_code": "U",
        "price_range": MoneyInterval.create(40, 60, "USD"),
    }
    ok, reason = sample_schema.validate(row)
    assert ok
    assert reason is None


def test_validate_invalid_row(sample_schema: Schema):
    row = {
        "id": "invalid_id",  # invalid integer
        "price": Money.create(50, "USD"),
        "description": "A great product",
        "rating": 4.8,
        "currency_code": "USD",  # invalid CHAR, length > 1
        "price_range": MoneyInterval.create(40, 60, "USD"),
    }
    ok, reason = sample_schema.validate(row)
    assert not ok
    assert (
        "Invalid value for field `id`" in reason
        or "Invalid value for field `currency_code`" in reason
    )
