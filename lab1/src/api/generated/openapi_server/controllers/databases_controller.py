import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.databases_post_request import DatabasesPostRequest  # noqa: E501
from openapi_server import util


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


def databases_post(databases_post_request):  # noqa: E501
    """Create a new database

     # noqa: E501

    :param databases_post_request: 
    :type databases_post_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        databases_post_request = DatabasesPostRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
