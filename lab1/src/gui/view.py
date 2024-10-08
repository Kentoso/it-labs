import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from service.database_service import AbstractDatabaseService


class View:
    def __init__(self, service: AbstractDatabaseService):
        self.service: AbstractDatabaseService = service
        self.databases = {}
        self.current_db = None
        self.root = tk.Tk()
        self.root.title("Database GUI")
        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        tk.Button(self.root, text="Create Database", command=self.create_database).pack(
            fill=tk.X
        )
        tk.Button(self.root, text="Use Database", command=self.use_database).pack(
            fill=tk.X
        )
        tk.Button(self.root, text="Create Table", command=self.create_table).pack(
            fill=tk.X
        )
        tk.Button(self.root, text="List Tables", command=self.list_tables).pack(
            fill=tk.X
        )
        tk.Button(
            self.root, text="Get Table Schema", command=self.get_table_schema
        ).pack(fill=tk.X)
        tk.Button(
            self.root, text="Insert into Table", command=self.insert_into_table
        ).pack(fill=tk.X)
        tk.Button(
            self.root, text="Select from Table", command=self.select_from_table
        ).pack(fill=tk.X)
        tk.Button(self.root, text="Update Table", command=self.update_table).pack(
            fill=tk.X
        )
        tk.Button(
            self.root, text="Delete from Table", command=self.delete_from_table
        ).pack(fill=tk.X)
        tk.Button(self.root, text="Union Tables", command=self.union_tables).pack(
            fill=tk.X
        )
        tk.Button(self.root, text="Save Database", command=self.save_database).pack(
            fill=tk.X
        )
        tk.Button(self.root, text="Load Database", command=self.load_database).pack(
            fill=tk.X
        )

    def create_database(self):
        db_name = simpledialog.askstring("Create Database", "Enter database name:")
        if db_name:
            try:
                self.service.create_database(self.databases, db_name)
                messagebox.showinfo("Success", f"Database '{db_name}' created.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def use_database(self):
        db_name = simpledialog.askstring("Use Database", "Enter database name:")
        if db_name:
            try:
                self.current_db = self.service.use_database(self.databases, db_name)
                messagebox.showinfo("Success", f"Using database '{db_name}'.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def create_table(self):
        table_name = simpledialog.askstring("Create Table", "Enter table name:")
        schema_str = simpledialog.askstring(
            "Create Table", "Enter schema (format: field1:type1,field2:type2):"
        )
        if table_name and schema_str:
            schema_fields = {
                field.split(":")[0].strip(): field.split(":")[1].strip()
                for field in schema_str.split(",")
            }
            try:
                self.service.create_table(
                    self.databases, self.current_db, table_name, schema_fields
                )
                messagebox.showinfo("Success", f"Table '{table_name}' created.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def list_tables(self):
        try:
            tables = self.service.list_tables(self.databases, self.current_db)
            if tables:
                messagebox.showinfo("Tables", f"Tables: {', '.join(tables)}")
            else:
                messagebox.showinfo("Tables", "No tables found.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def get_table_schema(self):
        table_name = simpledialog.askstring("Get Schema", "Enter table name:")
        if table_name:
            try:
                schema = self.service.get_table_schema(
                    self.databases, self.current_db, table_name
                )
                schema_str = ", ".join(
                    [f"{key}: {value}" for key, value in schema.items()]
                )
                messagebox.showinfo(
                    "Schema", f"Schema of table '{table_name}': {schema_str}"
                )
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def insert_into_table(self):
        table_name = simpledialog.askstring("Insert into Table", "Enter table name:")
        values_str = simpledialog.askstring(
            "Insert into Table", "Enter values (key=value pairs, comma-separated):"
        )
        if table_name and values_str:
            values = {
                k.strip(): v.strip()
                for k, v in (item.split("=") for item in values_str.split(","))
            }
            try:
                self.service.insert_into_table(
                    self.databases, self.current_db, table_name, values
                )
                messagebox.showinfo("Success", f"Inserted values into '{table_name}'.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def select_from_table(self):
        table_name = simpledialog.askstring("Select from Table", "Enter table name:")
        columns_str = simpledialog.askstring(
            "Select from Table", "Enter columns (comma-separated, optional):"
        )
        if table_name:
            try:
                columns = (
                    [col.strip() for col in columns_str.split(",")]
                    if columns_str
                    else []
                )
                results = self.service.select_from_table(
                    self.databases, self.current_db, table_name, columns
                )
                self.show_table_view(results)
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def show_table_view(self, results):
        if not results:
            messagebox.showinfo("Results", "No rows found.")
            return

        table_view = tk.Toplevel()
        table_view.title("Table View")

        tree = ttk.Treeview(table_view)
        tree.pack(fill=tk.BOTH, expand=True)

        columns = list(results[0].keys()) if results else []
        tree["columns"] = columns
        tree["show"] = "headings"
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for row in results:
            values = [row[col].__repr__() for col in columns]
            tree.insert("", "end", values=values)

    def update_table(self):
        table_name = simpledialog.askstring("Update Table", "Enter table name:")
        condition_str = simpledialog.askstring(
            "Update Table", "Enter condition (key=value pairs, comma-separated):"
        )
        new_values_str = simpledialog.askstring(
            "Update Table", "Enter new values (key=value pairs, comma-separated):"
        )
        if table_name and condition_str and new_values_str:
            try:
                condition = {
                    k.strip(): v.strip()
                    for k, v in (item.split("=") for item in condition_str.split(","))
                }
                new_values = {
                    k.strip(): v.strip()
                    for k, v in (item.split("=") for item in new_values_str.split(","))
                }
                self.service.update_table(
                    self.databases, self.current_db, table_name, condition, new_values
                )
                messagebox.showinfo("Success", f"Updated rows in '{table_name}'.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def delete_from_table(self):
        table_name = simpledialog.askstring("Delete from Table", "Enter table name:")
        condition_str = simpledialog.askstring(
            "Delete from Table", "Enter condition (key=value pairs, comma-separated):"
        )
        if table_name and condition_str:
            try:
                condition = {
                    k.strip(): v.strip()
                    for k, v in (item.split("=") for item in condition_str.split(","))
                }
                self.service.delete_from_table(
                    self.databases, self.current_db, table_name, condition
                )
                messagebox.showinfo("Success", f"Deleted rows from '{table_name}'.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def union_tables(self):
        table1_name = simpledialog.askstring("Union Tables", "Enter first table name:")
        table2_name = simpledialog.askstring("Union Tables", "Enter second table name:")
        if table1_name and table2_name:
            try:
                union_result = self.service.union_tables(
                    self.databases, self.current_db, table1_name, table2_name
                )
                self.show_table_view(union_result.rows)
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def save_database(self):
        file_path = simpledialog.askstring(
            "Save Database", "Enter file path to save database:"
        )
        if file_path:
            try:
                self.service.save_database(self.databases, self.current_db, file_path)
                messagebox.showinfo(
                    "Success", f"Database '{self.current_db}' saved to '{file_path}'."
                )
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def load_database(self):
        file_path = simpledialog.askstring(
            "Load Database", "Enter file path to load database:"
        )
        if file_path:
            try:
                db = self.service.load_database(self.databases, file_path)
                self.current_db = db.db_name
                messagebox.showinfo(
                    "Success",
                    f"Database '{self.current_db}' loaded and set as current database.",
                )
            except ValueError as e:
                messagebox.showerror("Error", str(e))
