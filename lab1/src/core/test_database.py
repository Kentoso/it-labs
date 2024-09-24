import pytest
from schema import Schema
from database import Database


def test_create_table():
    db = Database("test_db")
    schema = Schema({"name": "string", "age": "integer"})
    data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
    table = db.create_table("users", schema, data)
    assert table.name == "users"
    assert len(table.rows) == 2
    assert table.rows[0] == {"name": "Alice", "age": 25}
    assert table.rows[1] == {"name": "Bob", "age": 30}


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


def test_invalid_data():
    db = Database("test_db")
    schema = Schema({"name": "string", "age": "integer"})
    data = [{"name": "Alice", "age": "invalid"}]
    with pytest.raises(Exception) as e:
        db.create_table("users", schema, data)
    assert (
        str(e.value)
        == "Invalid data: Invalid row: Invalid value for field `age`: invalid"
    )
