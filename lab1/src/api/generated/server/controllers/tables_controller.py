import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from server.models.table_create import TableCreate  # noqa: E501
from server.models.table_union import TableUnion  # noqa: E501
from server import util


def databases_db_name_tables_get(db_name):  # noqa: E501
    """List all tables in a database

     # noqa: E501

    :param db_name: 
    :type db_name: str

    :rtype: Union[List[str], Tuple[List[str], int], Tuple[List[str], int, Dict[str, str]]
    """
    return 'do some magic!'


def databases_db_name_tables_post(db_name, table_create):  # noqa: E501
    """Create a new table in a database

     # noqa: E501

    :param db_name: 
    :type db_name: str
    :param table_create: 
    :type table_create: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        table_create = TableCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def databases_db_name_tables_table_name_schema_get(db_name, table_name):  # noqa: E501
    """Get the schema of a table

     # noqa: E501

    :param db_name: 
    :type db_name: str
    :param table_name: 
    :type table_name: str

    :rtype: Union[Dict[str, str], Tuple[Dict[str, str], int], Tuple[Dict[str, str], int, Dict[str, str]]
    """
    return 'do some magic!'


def databases_db_name_tables_union_post(db_name, table_union):  # noqa: E501
    """Perform a union operation between two tables

     # noqa: E501

    :param db_name: 
    :type db_name: str
    :param table_union: 
    :type table_union: dict | bytes

    :rtype: Union[List[Dict[str, str]], Tuple[List[Dict[str, str]], int], Tuple[List[Dict[str, str]], int, Dict[str, str]]
    """
    if connexion.request.is_json:
        table_union = TableUnion.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
