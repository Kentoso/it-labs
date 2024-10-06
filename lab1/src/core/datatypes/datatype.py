from abc import ABC, abstractmethod


class DataType(ABC):
    @abstractmethod
    def validate(self, *args) -> bool:
        pass
