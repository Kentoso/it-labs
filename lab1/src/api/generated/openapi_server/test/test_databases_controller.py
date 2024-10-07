import unittest

from flask import json

from openapi_server.models.databases_post_request import DatabasesPostRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDatabasesController(BaseTestCase):
    """DatabasesController integration test stubs"""

    def test_databases_db_name_delete(self):
        """Test case for databases_db_name_delete

        Delete a database
        """
        headers = { 
        }
        response = self.client.open(
            '/databases/{db_name}'.format(db_name='db_name_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_databases_db_name_get(self):
        """Test case for databases_db_name_get

        Get details of a database
        """
        headers = { 
        }
        response = self.client.open(
            '/databases/{db_name}'.format(db_name='db_name_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_databases_post(self):
        """Test case for databases_post

        Create a new database
        """
        databases_post_request = openapi_server.DatabasesPostRequest()
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/databases',
            method='POST',
            headers=headers,
            data=json.dumps(databases_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
