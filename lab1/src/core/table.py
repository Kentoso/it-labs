from schema import Schema


class Table:
    def __init__(self, name: str, schema: Schema):
        self.name: str = name
        self.schema: Schema = schema
        self.rows: list[dict] = []

    def insert(self, row: dict):
        ok, reason = self.schema.validate(row)
        if not ok:
            raise Exception(f"Invalid row: {reason}")

        self.rows.append(row)

    def validate(self, row: dict):
        return self.schema.validate(row)

    def select(self, columns: list[str]):
        if not columns:
            return self.rows

        return [{col: row[col] for col in columns} for row in self.rows]

    def delete(self, condition: dict):
        self.rows = [
            row
            for row in self.rows
            if not all(row[k] == v for k, v in condition.items())
        ]

    def update(self, condition: dict, new_values: dict):
        for row in self.rows:
            if all(row[k] == v for k, v in condition.items()):
                row.update(new_values)
