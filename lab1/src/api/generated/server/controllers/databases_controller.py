import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from server.models.database_create import DatabaseCreate  # noqa: E501
from server import util


def databases_db_name_delete(db_name):  # noqa: E501
    """Delete a database

     # noqa: E501

    :param db_name: 
    :type db_name: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def databases_db_name_get(db_name):  # noqa: E501
    """Get details of a database

     # noqa: E501

    :param db_name: 
    :type db_name: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def databases_post(database_create):  # noqa: E501
    """Create a new database

     # noqa: E501

    :param database_create: 
    :type database_create: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        database_create = DatabaseCreate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
