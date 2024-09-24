from functools import total_ordering


class Money:
    def __init__(self):
        self.value = 0
        self.currency = ""

    @staticmethod
    def create(value: int, currency: str) -> "Money":
        if value < 0:
            raise Exception("Money value cannot be negative")
        elif value > 10_000_000_000_000_00:
            raise Exception("Money value is too large")

        money = Money()
        money.value = value
        money.currency = currency
        return money

    def __add__(self, other):
        if self.currency != other.currency:
            raise Exception("Cannot add money with different currencies")

        return Money(self.value + other.value, self.currency)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise Exception("Cannot subtract money with different currencies")

        return Money(self.value - other.value, self.currency)

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
        return f"{self.value} {self.currency}"

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

        return Money.create(value, currency)


class MoneyInterval:
    def __init__(self):
        self.start = Money()
        self.end = Money()
        self.currency = ""

    @staticmethod
    def create(start: int | Money, end: int | Money, currency: str) -> "MoneyInterval":
        start_money = (
            start if isinstance(start, Money) else Money.create(start, currency)
        )
        end_money = end if isinstance(end, Money) else Money.create(end, currency)

        if start_money.currency != end_money.currency:
            raise Exception("Cannot create money interval with different currencies")

        if start_money > end_money:
            raise Exception("Money interval start is greater than end")

        interval = MoneyInterval()
        interval.start = start_money
        interval.end = end_money
        return interval

    def __str__(self) -> str:
        return f"{self.start} - {self.end} {self.currency}"
