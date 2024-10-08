import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from server.models.row_update import RowUpdate  # noqa: E501
from server import util


def databases_db_name_tables_table_name_rows_delete(db_name, table_name, condition):  # noqa: E501
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
    return 'do some magic!'


def databases_db_name_tables_table_name_rows_get(db_name, table_name, columns=None):  # noqa: E501
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
    return 'do some magic!'


def databases_db_name_tables_table_name_rows_post(db_name, table_name, request_body):  # noqa: E501
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
    return 'do some magic!'


def databases_db_name_tables_table_name_rows_put(db_name, table_name, row_update):  # noqa: E501
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
    if connexion.request.is_json:
        row_update = RowUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
