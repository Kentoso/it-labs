import connexion

from server.models.table_create import TableCreate  # noqa: E501
from server.models.table_union import TableUnion  # noqa: E501

from flask import g
from service.database_service import AbstractDatabaseService
import jsonpickle


def create_table(db_name, table_create):  # noqa: E501
    """Create a new table in a database

     # noqa: E501

    :param db_name:
    :type db_name: str
    :param table_create:
    :type table_create: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    print("CREATE TABLE")
    if connexion.request.is_json:
        table_create = TableCreate.from_dict(connexion.request.get_json())  # noqa: E501
        try:
            databases = {}
            databases[db_name] = database_service.load_database_json(
                databases, f"{db_name}.json"
            )
            print(databases)
            database_service.create_table(
                databases, db_name, table_create.table_name, table_create._schema
            )
            print(databases)
            database_service.save_database_json(databases, db_name, f"{db_name}.json")
            print(f"Table {table_create.table_name} created in database {db_name}")
            return None, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    return {"error": "Invalid input"}, 400


def delete_table(db_name, table_name):  # noqa: E501
    """Delete a table

     # noqa: E501

    :param db_name:
    :type db_name: str
    :param table_name:
    :type table_name: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    try:
        databases = {}
        database_service.load_database_json(databases, f"{db_name}.json")
        database_service.drop_table(databases, db_name, table_name)
        database_service.save_database_json(databases, db_name, f"{db_name}.json")
        return None, 204
    except ValueError as e:
        return {"error": str(e)}, 400


def get_table_schema(db_name, table_name):  # noqa: E501
    """Get the schema of a table

     # noqa: E501

    :param db_name:
    :type db_name: str
    :param table_name:
    :type table_name: str

    :rtype: Union[Dict[str, str], Tuple[Dict[str, str], int], Tuple[Dict[str, str], int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    try:
        databases = {}
        database_service.load_database_json(databases, f"{db_name}.json")
        schema = database_service.get_table_schema(databases, db_name, table_name)
        return jsonpickle.encode(schema), 200
    except ValueError as e:
        return {"error": str(e)}, 400


def list_tables(db_name):  # noqa: E501
    """List all tables in a database

     # noqa: E501

    :param db_name:
    :type db_name: str

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    try:
        databases = {}
        database_service.load_database_json(databases, f"{db_name}.json")
        tables = database_service.list_tables(databases, db_name)
        return tables, 200
    except ValueError as e:
        return {"error": str(e)}, 400


def perform_table_union(db_name, table_union):  # noqa: E501
    """Perform a union operation between two tables

     # noqa: E501

    :param db_name:
    :type db_name: str
    :param table_union:
    :type table_union: dict | bytes

    :rtype: Union[List[Dict[str, str]], Tuple[List[Dict[str, str]], int], Tuple[List[Dict[str, str]], int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    if connexion.request.is_json:
        table_union = TableUnion.from_dict(connexion.request.get_json())  # noqa: E501
        try:
            databases = {}
            database_service.load_database_json(databases, f"{db_name}.json")
            result = database_service.union_tables(
                databases, db_name, table_union.table1, table_union.table2
            )
            database_service.save_database_json(databases, db_name, f"{db_name}.json")
            return result.name, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    return {"error": "Invalid input"}, 400
