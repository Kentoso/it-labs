import os
import requests
import json

base_url = os.getenv("API_URL", "http://localhost:8080")


def test_end_to_end():
    db_name = "test_db"

    # Create a database
    response = requests.post(f"{base_url}/databases", json={"name": db_name})
    assert response.status_code == 201

    # Create a table
    schema = {
        "id": "integer",
        "price": "money",
        "description": "string",
        "rating": "real",
        "currency_code": "char",
        "price_range": "money_interval",
    }
    response = requests.post(
        f"{base_url}/databases/{db_name}/tables",
        json={"table_name": "products", "schema": schema},
    )
    assert response.status_code == 201

    # Get the table schema
    response = requests.get(f"{base_url}/databases/{db_name}/tables/products/schema")
    print(response.json())
    assert response.status_code == 200

    # Insert a row
    row = {
        "id": 123,
        "price": "50 USD",
        "description": "A great product",
        "rating": 4.8,
        "currency_code": "U",
        "price_range": "40 USD - 60 USD",
    }
    response = requests.post(
        f"{base_url}/databases/{db_name}/tables/products/rows", json=row
    )
    assert response.status_code == 201

    # Get the row
    row_filter = json.dumps(
        {
            "id": 123,
        }
    )
    response = requests.get(
        f"{base_url}/databases/{db_name}/tables/products/rows?filter={row_filter}"
    )
    assert response.status_code == 200
    assert response.json()[0] == row

    # Update the row
    row["price"] = "60 USD"
    response = requests.put(
        f"{base_url}/databases/{db_name}/tables/products/rows",
        json={"condition": {"id": 123}, "new_values": {"price": "60 USD"}},
    )
    assert response.status_code == 204

    # Get the updated row
    response = requests.get(
        f"{base_url}/databases/{db_name}/tables/products/rows?filter={row_filter}"
    )
    assert response.status_code == 200
    assert response.json()[0] == row

    # Delete the row
    response = requests.delete(
        f"{base_url}/databases/{db_name}/tables/products/rows?condition={row_filter}"
    )
    assert response.status_code == 204

    # Get the deleted row
    response = requests.get(
        f"{base_url}/databases/{db_name}/tables/products/rows?filter={row_filter}"
    )
    assert response.status_code == 200

    # Delete the table
    response = requests.delete(f"{base_url}/databases/{db_name}/tables/products")
    assert response.status_code == 204

    # List tables
    response = requests.get(f"{base_url}/databases/{db_name}/tables")
    assert response.status_code == 200
    assert response.json() == []

    # Delete the database
    response = requests.delete(f"{base_url}/databases/{db_name}")
    assert response.status_code == 204

    print("End-to-end test passed")


def test_table_union():
    db_name = "test_db_2"

    # Create a database
    response = requests.post(f"{base_url}/databases", json={"name": db_name})
    assert response.status_code == 201

    # Create a table
    schema = {
        "id": "integer",
        "price": "money",
        "description": "string",
        "rating": "real",
        "currency_code": "char",
        "price_range": "money_interval",
    }
    response = requests.post(
        f"{base_url}/databases/{db_name}/tables",
        json={"table_name": "products_1", "schema": schema},
    )
    assert response.status_code == 201

    response = requests.post(
        f"{base_url}/databases/{db_name}/tables",
        json={"table_name": "products_2", "schema": schema},
    )
    assert response.status_code == 201

    # Insert a row
    row = {
        "id": 1,
        "price": "50 USD",
        "description": "A great product",
        "rating": 4.8,
        "currency_code": "U",
        "price_range": "40 USD - 60 USD",
    }
    response = requests.post(
        f"{base_url}/databases/{db_name}/tables/products_1/rows", json=row
    )
    assert response.status_code == 201

    # Insert a row
    row = {
        "id": 2,
        "price": "25 USD",
        "description": "A not so great product",
        "rating": 128.2,
        "currency_code": "S",
        "price_range": "25 USD - 40 USD",
    }
    response = requests.post(
        f"{base_url}/databases/{db_name}/tables/products_2/rows", json=row
    )
    assert response.status_code == 201

    # Union tables
    response = requests.post(
        f"{base_url}/databases/{db_name}/tables/union",
        json={"table1": "products_1", "table2": "products_2"},
    )
    assert response.status_code == 200

    # Select from the union table
    response = requests.get(
        f"{base_url}/databases/{db_name}/tables/products_1_union_products_2/rows"
    )
    print(response.json())
    assert response.status_code == 200


def test_fail_creating_database_two_times():
    db_name = "test_db_3"

    # Create a database
    response = requests.post(f"{base_url}/databases", json={"name": db_name})
    assert response.status_code == 201

    # Create a database with the same name
    response = requests.post(f"{base_url}/databases", json={"name": db_name})
    assert response.status_code == 400
