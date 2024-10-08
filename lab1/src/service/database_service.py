from abc import ABC, abstractmethod
from core.database import Database
from core.schema import Schema
import logging
import json
import jsonpickle


class AbstractDatabaseService(ABC):
    @abstractmethod
    def create_database(self, databases: dict[str, Database], db_name):
        pass

    @abstractmethod
    def delete_database(self, databases: dict[str, Database], db_name):
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
        self,
        databases: dict[str, Database],
        current_db: str,
        table_name,
        columns=None,
        filter=None,
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

    @abstractmethod
    def save_database_json(
        self, databases: dict[str, Database], current_db: str, file_path
    ):
        pass

    @abstractmethod
    def load_database_json(self, databases: dict[str, Database], file_path):
        pass


logger = logging.getLogger(__name__)


class DatabaseService:
    def create_database(self, databases: dict[str, Database], db_name):
        if db_name in databases:
            raise ValueError(f"Database '{db_name}' already exists.")
        databases[db_name] = Database(db_name)

    def use_database(self, databases: dict[str, Database], db_name):
        if db_name not in databases:
            raise ValueError(f"Database '{db_name}' does not exist.")
        return db_name

    def delete_database(self, databases: dict[str, Database], db_name):
        if db_name not in databases:
            raise ValueError(f"Database '{db_name}' does not exist.")
        del databases[db_name]

    def create_table(
        self, databases: dict[str, Database], current_db: str, table_name, schema_fields
    ):
        if current_db is None:
            raise ValueError("No database selected.")
        schema = Schema(schema_fields)
        databases[current_db].create_table(table_name, schema)
        logger.info(f"Table {table_name} created in database {current_db}")

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
        self,
        databases: dict[str, Database],
        current_db: str,
        table_name,
        columns=None,
        filter=None,
    ):
        if current_db is None:
            raise ValueError("No database selected.")
        table = databases[current_db].get_table(table_name)
        rows = table.select(columns, filter)
        rows = [{k: v.to_json_value() for k, v in row.items()} for row in rows]
        return rows

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
        union = table1.union(table2)
        databases[current_db].tables.append(union)
        return union

    def save_database(self, databases: dict[str, Database], current_db: str, file_path):
        if current_db is None:
            raise ValueError("No database selected.")
        databases[current_db].save(file_path)

    def load_database(self, databases: dict[str, Database], file_path):
        db = Database.load(file_path)
        databases[db.db_name] = db
        return db

    def save_database_json(
        self, databases: dict[str, Database], current_db: str, file_path
    ):
        if current_db is None:
            raise ValueError("No database selected.")

        json_str = jsonpickle.encode(databases[current_db])
        with open(file_path, "w") as f:
            f.write(json_str)

    def load_database_json(self, databases: dict[str, Database], file_path):
        with open(file_path, "r") as f:
            read_data = f.read()
            db = jsonpickle.decode(read_data)
            databases[db.db_name] = db
            return db
