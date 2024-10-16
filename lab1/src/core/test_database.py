import pytest
from .schema import Schema
from .table import Table
from .database import Database
from . import datatypes


def test_create_table():
    db = Database("test_db")
    schema = Schema({"name": "string", "age": "integer"})
    data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
    table = db.create_table("users", schema, data)
    assert table.name == "users"
    assert len(table.rows) == 2
    assert table.rows[0] == {
        "name": datatypes.String("Alice"),
        "age": datatypes.Integer(25),
    }
    assert table.rows[1] == {
        "name": datatypes.String("Bob"),
        "age": datatypes.Integer(30),
    }


def test_create_table_duplicate():
    db = Database("test_db")
    schema = Schema({"name": "string", "age": "integer"})
    db.create_table("users", schema)
    with pytest.raises(Exception) as e:
        db.create_table("users", schema)
    assert str(e.value) == "Table users already exists"


def test_drop_table():
    db = Database("test_db")
    schema = Schema({"name": "string", "age": "integer"})
    db.create_table("users", schema)
    db.drop_table("users")
    with pytest.raises(Exception) as e:
        db.get_table("users")
    assert str(e.value) == "Table users not found"


def test_get_table():
    db = Database("test_db")
    schema = Schema({"name": "string", "age": "integer"})
    db.create_table("users", schema)
    table = db.get_table("users")
    assert table.name == "users"


def test_add_table():
    db = Database("test_db")
    schema = Schema({"name": "string", "age": "integer"})
    table = Table("users", schema)
    db.add_table(table)
    assert db.tables[0] == table


def test_invalid_data():
    db = Database("test_db")
    schema = Schema({"name": "string", "age": "integer"})
    data = [{"name": "Alice", "age": "invalid"}]
    with pytest.raises(Exception) as e:
        db.create_table("users", schema, data)
    assert (
        str(e.value)
        == "Invalid data: Invalid row: Invalid field age: Invalid integer: invalid"
    )
