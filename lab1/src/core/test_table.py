import pytest
from schema import Schema, DataTypeNames
from table import Table
import datatypes


@pytest.fixture
def sample_schema() -> Schema:
    return Schema(
        {
            "id": DataTypeNames.INTEGER,
            "name": DataTypeNames.STRING,
            "price": DataTypeNames.MONEY,
            "interval": DataTypeNames.MONEY_INTERVAL,
        }
    )


@pytest.fixture
def sample_table(sample_schema: Schema) -> Table:
    return Table("products", sample_schema)


def test_insert_valid_row(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": "100 USD",
        "interval": "100 USD - 200 USD",
    }
    sample_table.insert(row)
    assert len(sample_table.rows) == 1
    assert sample_table.rows[0] == {
        "id": datatypes.Integer(1),
        "name": datatypes.String("Widget"),
        "price": datatypes.Money("100 USD"),
        "interval": datatypes.MoneyInterval("100 USD - 200 USD"),
    }


def test_insert_invalid_money(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": "not_money",
        "interval": "100 USD - 200 USD",
    }
    with pytest.raises(Exception, match="Invalid row"):
        sample_table.insert(row)


def test_insert_invalid_money_interval(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": "100 USD",
        "interval": "not_money_interval",
    }
    with pytest.raises(Exception, match="Invalid row"):
        sample_table.insert(row)


def test_insert_invalid_integer(sample_table: Table):
    row = {
        "id": "not_an_integer",
        "name": "Widget",
        "price": "100 USD",
        "interval": "100 USD - 200 USD",
    }
    with pytest.raises(Exception, match="Invalid row"):
        sample_table.insert(row)


def test_validate_valid_row(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": "100 USD",
        "interval": "100 USD - 200 USD",
    }
    ok, reason = sample_table.validate(row)
    assert ok
    assert reason is None


def test_validate_invalid_row(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": "invalid_money",
        "interval": "100 USD - 200 USD",
    }
    ok, reason = sample_table.validate(row)
    assert not ok
    assert "Invalid field price" in reason


def test_select_columns(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": "100 USD",
        "interval": "100 USD - 200 USD",
    }
    sample_table.insert(row)
    result = sample_table.select(["id", "name"])
    expected = [{"id": datatypes.Integer(1), "name": datatypes.String("Widget")}]
    assert result == expected


def test_delete_row(sample_table: Table):
    row1 = {
        "id": 1,
        "name": "Widget",
        "price": "100 USD",
        "interval": "100 USD - 200 USD",
    }
    row2 = {
        "id": 2,
        "name": "Gadget",
        "price": "200 USD",
        "interval": "150 USD - 250 USD",
    }
    sample_table.insert(row1)
    sample_table.insert(row2)

    sample_table.delete({"id": 1})
    assert len(sample_table.rows) == 1
    assert sample_table.rows[0]["id"] == datatypes.Integer(2)


def test_update_row(sample_table: Table):
    row = {
        "id": 1,
        "name": "Widget",
        "price": "100 USD",
        "interval": "100 USD - 200 USD",
    }
    sample_table.insert(row)

    sample_table.update({"id": 1}, {"price": "150 USD"})
    assert sample_table.rows[0]["price"] == datatypes.Money("150 USD")


def test_union_success(sample_table: Table):
    row1 = {
        "id": 1,
        "name": "Widget",
        "price": "100 USD",
        "interval": "100 USD - 200 USD",
    }
    row2 = {
        "id": 2,
        "name": "Gadget",
        "price": "200 USD",
        "interval": "150 USD - 250 USD",
    }
    row3 = {
        "id": 3,
        "name": "Thing",
        "price": "300 USD",
        "interval": "250 USD - 350 USD",
    }
    row4 = {
        "id": 4,
        "name": "Doohickey",
        "price": "400 USD",
        "interval": "350 USD - 450 USD",
    }

    sample_table.insert(row1)
    sample_table.insert(row2)

    other_table = Table("other_products", sample_table.schema)
    other_table.insert(row3)
    other_table.insert(row4)

    result = sample_table.union(other_table)
    assert len(result.rows) == 4
    assert result.rows[0] == {
        "id": datatypes.Integer(1),
        "name": datatypes.String("Widget"),
        "price": datatypes.Money("100 USD"),
        "interval": datatypes.MoneyInterval("100 USD - 200 USD"),
    }
    assert result.rows[1] == {
        "id": datatypes.Integer(2),
        "name": datatypes.String("Gadget"),
        "price": datatypes.Money("200 USD"),
        "interval": datatypes.MoneyInterval("150 USD - 250 USD"),
    }
    assert result.rows[2] == {
        "id": datatypes.Integer(3),
        "name": datatypes.String("Thing"),
        "price": datatypes.Money("300 USD"),
        "interval": datatypes.MoneyInterval("250 USD - 350 USD"),
    }
    assert result.rows[3] == {
        "id": datatypes.Integer(4),
        "name": datatypes.String("Doohickey"),
        "price": datatypes.Money("400 USD"),
        "interval": datatypes.MoneyInterval("350 USD - 450 USD"),
    }


def test_union_failure(sample_table: Table):
    row1 = {
        "id": 1,
        "name": "Widget",
        "price": "100 USD",
        "interval": "100 USD - 200 USD",
    }
    row2 = {
        "id": 2,
        "name": "Gadget",
        "price": "200 USD",
        "interval": "150 USD - 250 USD",
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
        "other_products",
        Schema({"id": DataTypeNames.INTEGER, "name": DataTypeNames.STRING}),
    )
    other_table.insert(row3)
    other_table.insert(row4)

    with pytest.raises(Exception, match="Schemas do not match"):
        sample_table.union(other_table)


def test_rename(sample_table: Table):
    sample_table.rename("renamed_products")
    assert sample_table.name == "renamed_products"
