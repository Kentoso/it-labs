from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from server.models.base_model import Model
from server import util


class RowUpdate(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, condition=None, new_values=None):  # noqa: E501
        """RowUpdate - a model defined in OpenAPI

        :param condition: The condition of this RowUpdate.  # noqa: E501
        :type condition: Dict[str, str]
        :param new_values: The new_values of this RowUpdate.  # noqa: E501
        :type new_values: Dict[str, str]
        """
        self.openapi_types = {
            'condition': Dict[str, str],
            'new_values': Dict[str, str]
        }

        self.attribute_map = {
            'condition': 'condition',
            'new_values': 'new_values'
        }

        self._condition = condition
        self._new_values = new_values

    @classmethod
    def from_dict(cls, dikt) -> 'RowUpdate':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The RowUpdate of this RowUpdate.  # noqa: E501
        :rtype: RowUpdate
        """
        return util.deserialize_model(dikt, cls)

    @property
    def condition(self) -> Dict[str, str]:
        """Gets the condition of this RowUpdate.

        Condition to match rows to update as a dictionary  # noqa: E501

        :return: The condition of this RowUpdate.
        :rtype: Dict[str, str]
        """
        return self._condition

    @condition.setter
    def condition(self, condition: Dict[str, str]):
        """Sets the condition of this RowUpdate.

        Condition to match rows to update as a dictionary  # noqa: E501

        :param condition: The condition of this RowUpdate.
        :type condition: Dict[str, str]
        """

        self._condition = condition

    @property
    def new_values(self) -> Dict[str, str]:
        """Gets the new_values of this RowUpdate.

        New values to update in the matched rows as a dictionary  # noqa: E501

        :return: The new_values of this RowUpdate.
        :rtype: Dict[str, str]
        """
        return self._new_values

    @new_values.setter
    def new_values(self, new_values: Dict[str, str]):
        """Sets the new_values of this RowUpdate.

        New values to update in the matched rows as a dictionary  # noqa: E501

        :param new_values: The new_values of this RowUpdate.
        :type new_values: Dict[str, str]
        """

        self._new_values = new_values
