import connexion

from server.models.row_update import RowUpdate  # noqa: E501

from flask import g
from service.database_service import AbstractDatabaseService


def delete_rows(db_name, table_name, condition):  # noqa: E501
    """Delete rows from a table

     # noqa: E501

    :param db_name:
    :type db_name: str
    :param table_name:
    :type table_name: str
    :param condition:
    :type condition: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    try:
        condition = {
            k.strip(): v.strip()
            for k, v in (item.split("=") for item in condition.split(","))
        }
        databases = {}
        database_service.load_database(databases, f"{db_name}.pickle")
        database_service.delete_from_table(databases, db_name, table_name, condition)
        database_service.save_database(databases, db_name, f"{db_name}.pickle")
        return None, 204
    except ValueError as e:
        return {"error": str(e)}, 400


def insert_row(db_name, table_name, request_body):  # noqa: E501
    """Insert a row into a table

     # noqa: E501

    :param db_name:
    :type db_name: str
    :param table_name:
    :type table_name: str
    :param request_body:
    :type request_body: Dict[str, str]

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    try:
        databases = {}
        database_service.load_database(databases, f"{db_name}.pickle")
        database_service.insert_into_table(databases, db_name, table_name, request_body)
        database_service.save_database(databases, db_name, f"{db_name}.pickle")
        return None, 201
    except ValueError as e:
        return {"error": str(e)}, 400


def select_rows(db_name, table_name, columns=None):  # noqa: E501
    """Select rows from a table

     # noqa: E501

    :param db_name:
    :type db_name: str
    :param table_name:
    :type table_name: str
    :param columns:
    :type columns: str

    :rtype: Union[List[Dict[str, str]], Tuple[List[Dict[str, str]], int], Tuple[List[Dict[str, str]], int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    try:
        databases = {}
        database_service.load_database(databases, f"{db_name}.pickle")
        rows = database_service.select_from_table(
            databases, db_name, table_name, columns
        )
        return rows, 200
    except ValueError as e:
        return {"error": str(e)}, 400


def update_rows(db_name, table_name, row_update):  # noqa: E501
    """Update rows in a table

     # noqa: E501

    :param db_name:
    :type db_name: str
    :param table_name:
    :type table_name: str
    :param row_update:
    :type row_update: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    if connexion.request.is_json:
        row_update = RowUpdate.from_dict(connexion.request.get_json())  # noqa: E501
        try:
            databases = {}
            database_service.load_database(databases, f"{db_name}.pickle")
            database_service.update_table(
                databases,
                db_name,
                table_name,
                row_update.condition,
                row_update.new_values,
            )
            database_service.save_database(databases, db_name, f"{db_name}.pickle")
            return None, 204
        except ValueError as e:
            return {"error": str(e)}, 400

    return {"error": "Invalid input"}, 400
