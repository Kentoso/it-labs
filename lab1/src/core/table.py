from schema import Schema


class Table:
    def __init__(self, name: str, schema: Schema):
        self.name: str = name
        self.schema: Schema = schema
        self.rows: list[dict] = []

    def insert(self, row: dict):
        validated_row, reason = self.schema.validate(row)
        if not validated_row:
            raise Exception(f"Invalid row: {reason}")

        self.rows.append(validated_row)

    def validate(self, row: dict):
        return self.schema.validate(row)

    def select(self, columns: list[str]):
        if not columns:
            return self.rows

        return [{col: row[col] for col in columns} for row in self.rows]

    def delete(self, condition: dict):
        validated_condition, reason = self.schema.validate(condition)
        if not validated_condition:
            raise Exception(f"Invalid condition: {reason}")

        self.rows = [
            row
            for row in self.rows
            if not all(row[k] == v for k, v in validated_condition.items())
        ]

    def update(self, condition: dict, new_values: dict):
        validated_condition, reason = self.schema.validate(condition)
        if not validated_condition:
            raise Exception(f"Invalid condition: {reason}")

        validated_new_values, reason = self.schema.validate(new_values)
        if not validated_new_values:
            raise Exception(f"Invalid new values: {reason}")

        for row in self.rows:
            if all(row[k] == v for k, v in validated_condition.items()):
                row.update(validated_new_values)

    def rename(self, new_name: str):
        self.name = new_name

    def union(self, other: "Table"):
        if self.schema != other.schema:
            raise Exception("Schemas do not match")

        new_name = f"{self.name}_union_{other.name}"
        new_table = Table(new_name, self.schema)
        new_table.rows = self.rows + other.rows
        return new_table
