import pytest
from schema import Schema, DataType
from table import Table
from datatypes.money import Money, MoneyInterval


@pytest.fixture
def sample_schema() -> Schema:
    return Schema(
        {
            "id": DataType.INTEGER,
            "name": DataType.STRING,
            "price": DataType.MONEY,
            "interval": DataType.MONEY_INTERVAL,
        }
    )


@pytest.fixture
def sample_table(sample_schema: Schema) -> Table:
    return Table("products", sample_schema)


def test_insert_valid_row(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": Money.create(100, "USD"),
        "interval": MoneyInterval.create(100, 200, "USD"),
    }
    sample_table.insert(row)
    assert len(sample_table.rows) == 1
    assert sample_table.rows[0] == row


def test_insert_invalid_money(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": "not_money",
        "interval": MoneyInterval.create(100, 200, "USD"),
    }
    with pytest.raises(Exception, match="Invalid row"):
        sample_table.insert(row)


def test_insert_invalid_money_interval(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": Money.create(100, "USD"),
        "interval": "not_money_interval",
    }
    with pytest.raises(Exception, match="Invalid row"):
        sample_table.insert(row)


def test_insert_invalid_integer(sample_table: Table):
    row = {
        "id": "not_an_integer",
        "name": "Widget",
        "price": Money.create(100, "USD"),
        "interval": MoneyInterval.create(100, 200, "USD"),
    }
    with pytest.raises(Exception, match="Invalid row"):
        sample_table.insert(row)


def test_validate_valid_row(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": Money.create(100, "USD"),
        "interval": MoneyInterval.create(100, 200, "USD"),
    }
    ok, reason = sample_table.validate(row)
    assert ok
    assert reason is None


def test_validate_invalid_row(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": "invalid_money",
        "interval": MoneyInterval.create(100, 200, "USD"),
    }
    ok, reason = sample_table.validate(row)
    assert not ok
    assert "Invalid value for field `price`" in reason


def test_select_columns(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": Money.create(100, "USD"),
        "interval": MoneyInterval.create(100, 200, "USD"),
    }
    sample_table.insert(row)
    result = sample_table.select(["id", "name"])
    expected = [{"id": 1, "name": "Widget"}]
    assert result == expected


def test_delete_row(sample_table: Table):
    row1 = {
        "id": 1,
        "name": "Widget",
        "price": Money.create(100, "USD"),
        "interval": MoneyInterval.create(100, 200, "USD"),
    }
    row2 = {
        "id": 2,
        "name": "Gadget",
        "price": Money.create(200, "USD"),
        "interval": MoneyInterval.create(150, 250, "USD"),
    }
    sample_table.insert(row1)
    sample_table.insert(row2)

    sample_table.delete({"id": 1})
    assert len(sample_table.rows) == 1
    assert sample_table.rows[0]["id"] == 2


def test_update_row(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": Money.create(100, "USD"),
        "interval": MoneyInterval.create(100, 200, "USD"),
    }
    sample_table.insert(row)

    sample_table.update({"id": 1}, {"price": Money.create(150, "USD")})
    assert sample_table.rows[0]["price"] == Money.create(150, "USD")


def test_union_success(sample_table: Table):
    row1 = {
        "id": 1,
        "name": "Widget",
        "price": Money.create(100, "USD"),
        "interval": MoneyInterval.create(100, 200, "USD"),
    }
    row2 = {
        "id": 2,
        "name": "Gadget",
        "price": Money.create(200, "USD"),
        "interval": MoneyInterval.create(150, 250, "USD"),
    }
    row3 = {
        "id": 3,
        "name": "Thing",
        "price": Money.create(300, "USD"),
        "interval": MoneyInterval.create(250, 350, "USD"),
    }
    row4 = {
        "id": 4,
        "name": "Doohickey",
        "price": Money.create(400, "USD"),
        "interval": MoneyInterval.create(350, 450, "USD"),
    }

    sample_table.insert(row1)
    sample_table.insert(row2)

    other_table = Table("other_products", sample_table.schema)
    other_table.insert(row3)
    other_table.insert(row4)

    result = sample_table.union(other_table)
    assert len(result.rows) == 4
    assert result.rows[0] == row1
    assert result.rows[1] == row2
    assert result.rows[2] == row3
    assert result.rows[3] == row4


def test_union_failure(sample_table: Table):
    row1 = {
        "id": 1,
        "name": "Widget",
        "price": Money.create(100, "USD"),
        "interval": MoneyInterval.create(100, 200, "USD"),
    }
    row2 = {
        "id": 2,
        "name": "Gadget",
        "price": Money.create(200, "USD"),
        "interval": MoneyInterval.create(150, 250, "USD"),
    }
    row3 = {
        "id": 3,
        "name": "Thing",
    }
    row4 = {
        "id": 4,
        "name": "Doohickey",
    }

    sample_table.insert(row1)
    sample_table.insert(row2)

    other_table = Table(
        "other_products", Schema({"id": DataType.INTEGER, "name": DataType.STRING})
    )
    other_table.insert(row3)
    other_table.insert(row4)

    with pytest.raises(Exception, match="Schemas do not match"):
        sample_table.union(other_table)


def test_rename(sample_table: Table):
    sample_table.rename("renamed_products")
    assert sample_table.name == "renamed_products"
