import unittest

from flask import json

from openapi_server.models.databases_db_name_tables_post_request import DatabasesDbNameTablesPostRequest  # noqa: E501
from openapi_server.models.databases_db_name_tables_union_post_request import DatabasesDbNameTablesUnionPostRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestTablesController(BaseTestCase):
    """TablesController integration test stubs"""

    def test_databases_db_name_tables_get(self):
        """Test case for databases_db_name_tables_get

        List all tables in a database
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/databases/{db_name}/tables'.format(db_name='db_name_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_databases_db_name_tables_post(self):
        """Test case for databases_db_name_tables_post

        Create a new table in a database
        """
        databases_db_name_tables_post_request = openapi_server.DatabasesDbNameTablesPostRequest()
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/databases/{db_name}/tables'.format(db_name='db_name_example'),
            method='POST',
            headers=headers,
            data=json.dumps(databases_db_name_tables_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_databases_db_name_tables_table_name_schema_get(self):
        """Test case for databases_db_name_tables_table_name_schema_get

        Get the schema of a table
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/databases/{db_name}/tables/{table_name}/schema'.format(db_name='db_name_example', table_name='table_name_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_databases_db_name_tables_union_post(self):
        """Test case for databases_db_name_tables_union_post

        Perform a union operation between two tables
        """
        databases_db_name_tables_union_post_request = openapi_server.DatabasesDbNameTablesUnionPostRequest()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/databases/{db_name}/tables/union'.format(db_name='db_name_example'),
            method='POST',
            headers=headers,
            data=json.dumps(databases_db_name_tables_union_post_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
