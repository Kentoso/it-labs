from functools import total_ordering
from core.datatypes.datatype import DataType


class Money(DataType):
    def __init__(self, money: str = "0 USD"):
        # value is stored in cents
        self.value, self.currency = Money.parse(money)
        if not self.validate():
            print("VALUE:", type(self.value), self.value)

    def validate(self) -> bool:
        return (
            isinstance(self.value, int)
            and self.value >= 0
            and self.value <= 10_000_000_000_000_00
            and isinstance(self.currency, str)
        )

    def __eq__(self, other):
        return (
            isinstance(other, Money)
            and self.value == other.value
            and self.currency == other.currency
        )

    @total_ordering
    def __lt__(self, other):
        if self.currency != other.currency:
            raise Exception("Cannot compare money with different currencies")

        return self.value < other.value

    def __str__(self) -> str:
        cents = self.value % 100
        if cents > 0:
            return f"{self.value // 100}.{cents} {self.currency}"
        else:
            return f"{self.value // 100} {self.currency}"

    def to_json_value(self):
        return self.__str__()

    def __repr__(self) -> str:
        return f"Money({self})"

    @staticmethod
    def parse(s: str):
        value, currency = s.split()
        if not value.isdigit():
            raise Exception("Money value is not a number")

        if not currency.isalpha():
            raise Exception("Money currency is not a string")

        value = value.replace(",", "").replace("_", "")

        if "." not in value:
            value = int(value) * 100
        else:
            value = int(value)

        return value, currency


class MoneyInterval(DataType):
    def __init__(self, interval: str):
        self.start, self.end = MoneyInterval.parse(interval)

        if not self.validate():
            raise ValueError(f"Invalid money interval: {self.start} - {self.end}")

    def validate(self) -> bool:
        return self.start.currency == self.end.currency and (
            self.start < self.end or self.start == self.end
        )

    def __str__(self) -> str:
        return f"{self.start} - {self.end}"

    def to_json_value(self):
        return self.__str__()

    def __repr__(self) -> str:
        return f"MoneyInterval({self})"

    def parse(s: str):
        start, end = s.split(" - ")
        return Money(start), Money(end)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, MoneyInterval)
            and self.start == other.start
            and self.end == other.end
        )
