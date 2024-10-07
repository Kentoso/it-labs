import unittest

from flask import json

from openapi_server.models.databases_db_name_tables_table_name_rows_put_request import DatabasesDbNameTablesTableNameRowsPutRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestRowsController(BaseTestCase):
    """RowsController integration test stubs"""

    def test_databases_db_name_tables_table_name_rows_delete(self):
        """Test case for databases_db_name_tables_table_name_rows_delete

        Delete rows from a table
        """
        query_string = [('condition', 'condition_example')]
        headers = { 
        }
        response = self.client.open(
            '/databases/{db_name}/tables/{table_name}/rows'.format(db_name='db_name_example', table_name='table_name_example'),
            method='DELETE',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_databases_db_name_tables_table_name_rows_get(self):
        """Test case for databases_db_name_tables_table_name_rows_get

        Select rows from a table
        """
        query_string = [('columns', 'columns_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/databases/{db_name}/tables/{table_name}/rows'.format(db_name='db_name_example', table_name='table_name_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_databases_db_name_tables_table_name_rows_post(self):
        """Test case for databases_db_name_tables_table_name_rows_post

        Insert a row into a table
        """
        request_body = {'key': 'request_body_example'}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/databases/{db_name}/tables/{table_name}/rows'.format(db_name='db_name_example', table_name='table_name_example'),
            method='POST',
            headers=headers,
            data=json.dumps(request_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_databases_db_name_tables_table_name_rows_put(self):
        """Test case for databases_db_name_tables_table_name_rows_put

        Update rows in a table
        """
        databases_db_name_tables_table_name_rows_put_request = openapi_server.DatabasesDbNameTablesTableNameRowsPutRequest()
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/databases/{db_name}/tables/{table_name}/rows'.format(db_name='db_name_example', table_name='table_name_example'),
            method='PUT',
            headers=headers,
            data=json.dumps(databases_db_name_tables_table_name_rows_put_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
