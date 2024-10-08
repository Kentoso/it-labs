from abc import ABC, abstractmethod
from core.database import Database
from core.schema import Schema


class AbstractDatabaseService(ABC):
    @abstractmethod
    def create_database(self, databases: dict[str, Database], db_name):
        pass

    @abstractmethod
    def use_database(self, databases: dict[str, Database], db_name):
        pass

    @abstractmethod
    def create_table(
        self, databases: dict[str, Database], current_db: str, table_name, schema_fields
    ):
        pass

    @abstractmethod
    def list_tables(self, databases: dict[str, Database], current_db):
        pass

    @abstractmethod
    def get_table_schema(
        self, databases: dict[str, Database], current_db: str, table_name
    ):
        pass

    @abstractmethod
    def insert_into_table(
        self, databases: dict[str, Database], current_db: str, table_name, values
    ):
        pass

    @abstractmethod
    def select_from_table(
        self, databases: dict[str, Database], current_db: str, table_name, columns=None
    ):
        pass

    @abstractmethod
    def update_table(
        self,
        databases: dict[str, Database],
        current_db: str,
        table_name,
        condition,
        new_values,
    ):
        pass

    @abstractmethod
    def delete_from_table(
        self, databases: dict[str, Database], current_db: str, table_name, condition
    ):
        pass

    @abstractmethod
    def union_tables(
        self, databases: dict[str, Database], current_db: str, table1_name, table2_name
    ):
        pass

    @abstractmethod
    def save_database(self, databases: dict[str, Database], current_db: str, file_path):
        pass

    @abstractmethod
    def load_database(self, databases: dict[str, Database], file_path):
        pass


class DatabaseService:
    def create_database(self, databases: dict[str, Database], db_name):
        if db_name in databases:
            raise ValueError(f"Database '{db_name}' already exists.")
        databases[db_name] = Database(db_name)

    def use_database(self, databases: dict[str, Database], db_name):
        if db_name not in databases:
            raise ValueError(f"Database '{db_name}' does not exist.")
        return db_name

    def create_table(
        self, databases: dict[str, Database], current_db: str, table_name, schema_fields
    ):
        if current_db is None:
            raise ValueError("No database selected.")
        schema = Schema(schema_fields)
        databases[current_db].create_table(table_name, schema)

    def list_tables(self, databases: dict[str, Database], current_db):
        if current_db is None:
            raise ValueError("No database selected.")
        return [table.name for table in databases[current_db].tables]

    def get_table_schema(
        self, databases: dict[str, Database], current_db: str, table_name
    ):
        if current_db is None:
            raise ValueError("No database selected.")
        table = databases[current_db].get_table(table_name)
        return table.schema.fields

    def insert_into_table(
        self, databases: dict[str, Database], current_db: str, table_name, values
    ):
        if current_db is None:
            raise ValueError("No database selected.")
        table = databases[current_db].get_table(table_name)
        table.insert(values)

    def select_from_table(
        self, databases: dict[str, Database], current_db: str, table_name, columns=None
    ):
        if current_db is None:
            raise ValueError("No database selected.")
        print(databases[current_db].tables)
        table = databases[current_db].get_table(table_name)
        return table.select(columns)

    def update_table(
        self,
        databases: dict[str, Database],
        current_db: str,
        table_name,
        condition,
        new_values,
    ):
        if current_db is None:
            raise ValueError("No database selected.")
        table = databases[current_db].get_table(table_name)
        table.update(condition, new_values)

    def delete_from_table(
        self, databases: dict[str, Database], current_db: str, table_name, condition
    ):
        if current_db is None:
            raise ValueError("No database selected.")
        table = databases[current_db].get_table(table_name)

        table.delete(condition)

    def union_tables(
        self, databases: dict[str, Database], current_db: str, table1_name, table2_name
    ):
        if current_db is None:
            raise ValueError("No database selected.")
        table1 = databases[current_db].get_table(table1_name)
        table2 = databases[current_db].get_table(table2_name)
        return table1.union(table2)

    def save_database(self, databases: dict[str, Database], current_db: str, file_path):
        if current_db is None:
            raise ValueError("No database selected.")
        databases[current_db].save(file_path)

    def load_database(self, databases: dict[str, Database], file_path):
        db = Database.load(file_path)
        databases[db.db_name] = db
        return db.db_name
