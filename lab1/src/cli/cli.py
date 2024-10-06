import argparse
import core.datatypes as datatypes
from core.database import Database
from core.schema import Schema
from enum import Enum

# Store databases in memory for simplicity
databases = {}
current_db = None


class DataTypeNames(str, Enum):
    INTEGER = "integer"
    REAL = "real"
    CHAR = "char"
    STRING = "string"
    MONEY = "money"
    MONEY_INTERVAL = "money_interval"


name_to_datatype = {
    DataTypeNames.INTEGER: datatypes.Integer,
    DataTypeNames.REAL: datatypes.Real,
    DataTypeNames.CHAR: datatypes.Char,
    DataTypeNames.STRING: datatypes.String,
    DataTypeNames.MONEY: datatypes.Money,
    DataTypeNames.MONEY_INTERVAL: datatypes.MoneyInterval,
}


def create_database(db_name):
    if db_name in databases:
        print(f"Database '{db_name}' already exists.")
    else:
        databases[db_name] = Database(db_name)
        print(f"Database '{db_name}' created.")


def use_database(db_name):
    global current_db
    if db_name not in databases:
        print(f"Database '{db_name}' does not exist.")
    else:
        current_db = db_name
        print(f"Using database '{db_name}'.")


def create_table(table_name, schema_str):
    if current_db is None:
        print("No database selected. Use 'use <db_name>' to select a database.")
        return

    schema_fields = {
        field.split(":")[0].strip(): field.split(":")[1].strip()
        for field in schema_str.split(",")
    }
    for field_name, field_type in schema_fields.items():
        if field_type not in name_to_datatype:
            print(f"Invalid data type '{field_type}' for field '{field_name}'.")
            return

    schema = Schema(schema_fields)
    try:
        databases[current_db].create_table(table_name, schema)
        print(f"Table '{table_name}' created in database '{current_db}'.")
    except Exception as e:
        print(f"Error creating table: {e}")


def list_tables():
    if current_db is None:
        print("No database selected. Use 'use <db_name>' to select a database.")
        return

    tables = [table.name for table in databases[current_db].tables]
    if tables:
        print(f"Tables in '{current_db}': {', '.join(tables)}")
    else:
        print(f"No tables found in '{current_db}'.")


def get_table_schema(table_name):
    if current_db is None:
        print("No database selected. Use 'use <db_name>' to select a database.")
        return

    try:
        table = databases[current_db].get_table(table_name)
        schema = table.schema.fields
        schema_str = ", ".join([f"{key}: {value}" for key, value in schema.items()])
        print(f"Schema of table '{table_name}': {schema_str}")
    except Exception as e:
        print(f"Error getting schema: {e}")


def insert_into_table(table_name, values_str):
    if current_db is None:
        print("No database selected. Use 'use <db_name>' to select a database.")
        return

    try:
        table = databases[current_db].get_table(table_name)
        values = {
            k.strip(): v.strip()
            for k, v in (item.split("=") for item in values_str.split(","))
        }
        table.insert(values)
        print(f"Inserted values into '{table_name}'.")
    except Exception as e:
        print(f"Error inserting into table: {e}")


def select_from_table(table_name, columns_str):
    if current_db is None:
        print("No database selected. Use 'use <db_name>' to select a database.")
        return

    try:
        table = databases[current_db].get_table(table_name)
        columns = [col.strip() for col in columns_str.split(",")] if columns_str else []
        results = table.select(columns)
        print(f"Selected rows from '{table_name}': {results}")
    except Exception as e:
        print(f"Error selecting from table: {e}")


def update_table(table_name, condition_str, new_values_str):
    if current_db is None:
        print("No database selected. Use 'use <db_name>' to select a database.")
        return

    try:
        table = databases[current_db].get_table(table_name)
        condition = {
            k.strip(): v.strip()
            for k, v in (item.split("=") for item in condition_str.split(","))
        }
        new_values = {
            k.strip(): v.strip()
            for k, v in (item.split("=") for item in new_values_str.split(","))
        }
        table.update(condition, new_values)
        print(f"Updated rows in '{table_name}'.")
    except Exception as e:
        print(f"Error updating table: {e}")


def delete_from_table(table_name, condition_str):
    if current_db is None:
        print("No database selected. Use 'use <db_name>' to select a database.")
        return

    try:
        table = databases[current_db].get_table(table_name)
        condition = {
            k.strip(): v.strip()
            for k, v in (item.split("=") for item in condition_str.split(","))
        }
        table.delete(condition)
        print(f"Deleted rows from '{table_name}'.")
    except Exception as e:
        print(f"Error deleting from table: {e}")


def union_tables(table1_name, table2_name):
    if current_db is None:
        print("No database selected. Use 'use <db_name>' to select a database.")
        return

    try:
        table1 = databases[current_db].get_table(table1_name)
        table2 = databases[current_db].get_table(table2_name)
        union_result = table1.union(table2)
        print(f"Union of '{table1_name}' and '{table2_name}': {union_result.rows}")
    except Exception as e:
        print(f"Error performing union: {e}")


def save_database(file_path):
    if current_db is None:
        print("No database selected. Use 'use <db_name>' to select a database.")
        return

    try:
        databases[current_db].save(file_path)
        print(f"Database '{current_db}' saved to '{file_path}'.")
    except Exception as e:
        print(f"Error saving database: {e}")


def load_database(file_path):
    global current_db
    try:
        db = Database.load(file_path)
        databases[db.db_name] = db
        current_db = db.db_name
        print(f"Database '{db.db_name}' loaded and set as current database.")
    except Exception as e:
        print(f"Error loading database: {e}")


def interactive_mode():
    print(
        "Entering interactive mode. Type 'exit' to quit or 'help' to see available commands."
    )
    while True:
        try:
            user_input = input("dbms> ").strip()
            if user_input.lower() == "exit":
                print("Exiting interactive mode.")
                break
            elif user_input.lower() == "help":
                print("Available commands:")
                print("  create_db <db_name> - Create a new database")
                print("  use <db_name> - Set the current active database")
                print(
                    "  create_table <table_name> <schema> - Create a new table with a schema (format: field1:type1,field2:type2)"
                )
                print("  list_tables - List all tables in the current database")
                print("  get_schema <table_name> - Get the schema of a table")
                print(
                    "  insert <table_name> <values> - Insert data into a table (key=value pairs, comma-separated)"
                )
                print(
                    "  select <table_name> [columns] - Select data from a table (optional columns, comma-separated)"
                )
                print(
                    "  update <table_name> <condition> <new_values> - Update data in a table (key=value pairs, comma-separated)"
                )
                print(
                    "  delete <table_name> <condition> - Delete data from a table (key=value pairs, comma-separated)"
                )
                print(
                    "  union <table1_name> <table2_name> - Perform union operation on two tables"
                )
                print("  save <file_path> - Save the current database to a file")
                print(
                    "  load <file_path> - Load a database from a file and set it as current"
                )
                print("  exit - Exit the interactive mode")
            else:
                args = user_input.split()
                command = args[0]
                if command == "create_db" and len(args) == 2:
                    create_database(args[1])
                elif command == "use" and len(args) == 2:
                    use_database(args[1])
                elif command == "create_table" and len(args) == 3:
                    create_table(args[1], args[2])
                elif command == "list_tables" and len(args) == 1:
                    list_tables()
                elif command == "get_schema" and len(args) == 2:
                    get_table_schema(args[1])
                elif command == "insert" and len(args) == 3:
                    insert_into_table(args[1], args[2])
                elif command == "select" and len(args) >= 2:
                    columns = args[2] if len(args) == 3 else None
                    select_from_table(args[1], columns)
                elif command == "update" and len(args) == 4:
                    update_table(args[1], args[2], args[3])
                elif command == "delete" and len(args) == 3:
                    delete_from_table(args[1], args[2])
                elif command == "union" and len(args) == 3:
                    union_tables(args[1], args[2])
                elif command == "save" and len(args) == 2:
                    save_database(args[1])
                elif command == "load" and len(args) == 2:
                    load_database(args[1])
                else:
                    print(
                        "Invalid command or arguments. Type 'help' for a list of commands."
                    )
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple CLI for your DBMS.")
    parser.add_argument(
        "--interactive", action="store_true", help="Start the DBMS in interactive mode."
    )
    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    else:
        print("Please use --interactive to start the DBMS in interactive mode.")
