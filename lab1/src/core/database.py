from core.table import Table
from core.schema import Schema


class Database:
    def __init__(self, db_name: str):
        self.db_name: str = db_name
        self.tables: list[Table] = []

    def create_table(self, table_name: str, schema: Schema, data: list[dict] = []):
        if table_name in [t.name for t in self.tables]:
            raise Exception(f"Table {table_name} already exists")

        table = Table(table_name, schema)
        try:
            for row in data:
                table.insert(row)
        except Exception as e:
            raise Exception(f"Invalid data: {e}")

        self.tables.append(table)

        return table

    def add_table(self, table: Table):
        if table.name in [t.name for t in self.tables]:
            raise Exception(f"Table {table.name} already exists")

        self.tables.append(table)

    def drop_table(self, table_name: str):
        for i, table in enumerate(self.tables):
            if table.name == table_name:
                del self.tables[i]
                return

        raise Exception(f"Table {table_name} not found")

    def get_table(self, table_name: str):
        for table in self.tables:
            if table.name == table_name:
                return table

        raise Exception(f"Table {table_name} not found")
