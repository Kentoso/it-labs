import os

import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from server.models.database_create import DatabaseCreate  # noqa: E501
from server import util
from flask import g
from service.database_service import AbstractDatabaseService


def create_database(database_create):  # noqa: E501
    """Create a new database

     # noqa: E501

    :param database_create:
    :type database_create: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    if connexion.request.is_json:
        database_create = DatabaseCreate.from_dict(connexion.request.get_json())
        try:
            databases = {}
            database_service.create_database(databases, database_create.db_name)
            database_service.save_database(
                databases, database_create.db_name, f"{database_create.db_name}.pickle"
            )
            return None, 201
        except ValueError as e:
            return {"error": str(e)}, 400
    return {"error": "Invalid input"}, 400


def delete_database(db_name):  # noqa: E501
    """Delete a database

     # noqa: E501

    :param db_name:
    :type db_name: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    database_service: AbstractDatabaseService = g.database_service

    try:
        database_service.load_database(f"{db_name}.pickle")
        os.remove(f"{db_name}.pickle")
        return None, 204
    except FileNotFoundError:
        return {"error": f"Database {db_name} not found"}, 404
