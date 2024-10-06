import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from core.database import Database
from core.schema import Schema
import core.datatypes as datatypes
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


def create_database():
    global databases
    db_name = simpledialog.askstring("Create Database", "Enter database name:")
    if db_name:
        if db_name in databases:
            messagebox.showerror("Error", f"Database '{db_name}' already exists.")
        else:
            databases[db_name] = Database(db_name)
            messagebox.showinfo("Success", f"Database '{db_name}' created.")


def use_database():
    global current_db
    db_name = simpledialog.askstring("Use Database", "Enter database name:")
    if db_name:
        if db_name not in databases:
            messagebox.showerror("Error", f"Database '{db_name}' does not exist.")
        else:
            current_db = db_name
            messagebox.showinfo("Success", f"Using database '{db_name}'.")


def create_table():
    global current_db
    if current_db is None:
        messagebox.showerror(
            "Error", "No database selected. Use 'Use Database' to select a database."
        )
        return

    table_name = simpledialog.askstring("Create Table", "Enter table name:")
    schema_str = simpledialog.askstring(
        "Create Table", "Enter schema (format: field1:type1,field2:type2):"
    )
    if table_name and schema_str:
        schema_fields = {
            field.split(":")[0].strip(): field.split(":")[1].strip()
            for field in schema_str.split(",")
        }
        for field_name, field_type in schema_fields.items():
            if field_type not in name_to_datatype:
                messagebox.showerror(
                    "Error",
                    f"Invalid data type '{field_type}' for field '{field_name}'.",
                )
                return

        schema = Schema(schema_fields)
        try:
            databases[current_db].create_table(table_name, schema)
            messagebox.showinfo(
                "Success", f"Table '{table_name}' created in database '{current_db}'."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error creating table: {e}")


def list_tables():
    global current_db
    if current_db is None:
        messagebox.showerror(
            "Error", "No database selected. Use 'Use Database' to select a database."
        )
        return

    tables = [table.name for table in databases[current_db].tables]
    if tables:
        messagebox.showinfo("Tables", f"Tables in '{current_db}': {', '.join(tables)}")
    else:
        messagebox.showinfo("Tables", f"No tables found in '{current_db}'.")


def get_table_schema():
    global current_db
    if current_db is None:
        messagebox.showerror(
            "Error", "No database selected. Use 'Use Database' to select a database."
        )
        return

    table_name = simpledialog.askstring("Get Schema", "Enter table name:")
    if table_name:
        try:
            table = databases[current_db].get_table(table_name)
            schema = table.schema.fields
            schema_str = ", ".join([f"{key}: {value}" for key, value in schema.items()])
            messagebox.showinfo(
                "Schema", f"Schema of table '{table_name}': {schema_str}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error getting schema: {e}")


def insert_into_table():
    global current_db
    if current_db is None:
        messagebox.showerror(
            "Error", "No database selected. Use 'Use Database' to select a database."
        )
        return

    table_name = simpledialog.askstring("Insert into Table", "Enter table name:")
    values_str = simpledialog.askstring(
        "Insert into Table", "Enter values (key=value pairs, comma-separated):"
    )
    if table_name and values_str:
        try:
            table = databases[current_db].get_table(table_name)
            values = {
                k.strip(): v.strip()
                for k, v in (item.split("=") for item in values_str.split(","))
            }
            table.insert(values)
            messagebox.showinfo("Success", f"Inserted values into '{table_name}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting into table: {e}")


def select_from_table():
    global current_db
    if current_db is None:
        messagebox.showerror(
            "Error", "No database selected. Use 'Use Database' to select a database."
        )
        return

    table_name = simpledialog.askstring("Select from Table", "Enter table name:")
    columns_str = simpledialog.askstring(
        "Select from Table", "Enter columns (comma-separated, optional):"
    )
    if table_name:
        try:
            table = databases[current_db].get_table(table_name)
            columns = (
                [col.strip() for col in columns_str.split(",")] if columns_str else []
            )
            results = table.select(columns)
            show_table_view(results)
        except Exception as e:
            messagebox.showerror("Error", f"Error selecting from table: {e}")


def show_table_view(results):
    if not results:
        messagebox.showinfo("Results", "No rows found.")
        return

    table_view = tk.Toplevel()
    table_view.title("Table View")

    tree = ttk.Treeview(table_view)
    tree.pack(fill=tk.BOTH, expand=True)

    # Add columns to the tree view
    columns = list(results[0].keys()) if results else []
    tree["columns"] = columns
    tree["show"] = "headings"
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    # Add rows to the tree view
    for row in results:
        values = [row[col] for col in columns]
        tree.insert("", "end", values=values)


def update_table():
    global current_db
    if current_db is None:
        messagebox.showerror(
            "Error", "No database selected. Use 'Use Database' to select a database."
        )
        return

    table_name = simpledialog.askstring("Update Table", "Enter table name:")
    condition_str = simpledialog.askstring(
        "Update Table", "Enter condition (key=value pairs, comma-separated):"
    )
    new_values_str = simpledialog.askstring(
        "Update Table", "Enter new values (key=value pairs, comma-separated):"
    )
    if table_name and condition_str and new_values_str:
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
            messagebox.showinfo("Success", f"Updated rows in '{table_name}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating table: {e}")


def delete_from_table():
    global current_db
    if current_db is None:
        messagebox.showerror(
            "Error", "No database selected. Use 'Use Database' to select a database."
        )
        return

    table_name = simpledialog.askstring("Delete from Table", "Enter table name:")
    condition_str = simpledialog.askstring(
        "Delete from Table", "Enter condition (key=value pairs, comma-separated):"
    )
    if table_name and condition_str:
        try:
            table = databases[current_db].get_table(table_name)
            condition = {
                k.strip(): v.strip()
                for k, v in (item.split("=") for item in condition_str.split(","))
            }
            table.delete(condition)
            messagebox.showinfo("Success", f"Deleted rows from '{table_name}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting from table: {e}")


def union_tables():
    global current_db
    if current_db is None:
        messagebox.showerror(
            "Error", "No database selected. Use 'Use Database' to select a database."
        )
        return

    table1_name = simpledialog.askstring("Union Tables", "Enter first table name:")
    table2_name = simpledialog.askstring("Union Tables", "Enter second table name:")
    if table1_name and table2_name:
        try:
            table1 = databases[current_db].get_table(table1_name)
            table2 = databases[current_db].get_table(table2_name)
            union_result = table1.union(table2)
            show_table_view(union_result.rows)
        except Exception as e:
            messagebox.showerror("Error", f"Error performing union: {e}")


def save_database():
    global current_db
    if current_db is None:
        messagebox.showerror(
            "Error", "No database selected. Use 'Use Database' to select a database."
        )
        return

    file_path = simpledialog.askstring(
        "Save Database", "Enter file path to save database:"
    )
    if file_path:
        try:
            databases[current_db].save(file_path)
            messagebox.showinfo(
                "Success", f"Database '{current_db}' saved to '{file_path}'."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error saving database: {e}")


def load_database():
    global current_db
    file_path = simpledialog.askstring(
        "Load Database", "Enter file path to load database:"
    )
    if file_path:
        try:
            db = Database.load(file_path)
            databases[db.db_name] = db
            current_db = db.db_name
            messagebox.showinfo(
                "Success",
                f"Database '{db.db_name}' loaded and set as current database.",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error loading database: {e}")


def main():
    root = tk.Tk()
    root.title("GUI")

    tk.Button(root, text="Create Database", command=create_database).pack(fill=tk.X)
    tk.Button(root, text="Use Database", command=use_database).pack(fill=tk.X)
    tk.Button(root, text="Create Table", command=create_table).pack(fill=tk.X)
    tk.Button(root, text="List Tables", command=list_tables).pack(fill=tk.X)
    tk.Button(root, text="Get Table Schema", command=get_table_schema).pack(fill=tk.X)
    tk.Button(root, text="Insert into Table", command=insert_into_table).pack(fill=tk.X)
    tk.Button(root, text="Select from Table", command=select_from_table).pack(fill=tk.X)
    tk.Button(root, text="Update Table", command=update_table).pack(fill=tk.X)
    tk.Button(root, text="Delete from Table", command=delete_from_table).pack(fill=tk.X)
    tk.Button(root, text="Union Tables", command=union_tables).pack(fill=tk.X)
    tk.Button(root, text="Save Database", command=save_database).pack(fill=tk.X)
    tk.Button(root, text="Load Database", command=load_database).pack(fill=tk.X)

    root.mainloop()


if __name__ == "__main__":
    main()
