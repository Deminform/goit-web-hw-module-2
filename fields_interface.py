from abc import ABC, abstractmethod


class Field(ABC):
    def __init__(self, value):
        self._value = value

    @abstractmethod
    def __str__(self):
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Validate(ABC):
    @abstractmethod
    def _validate(self, value):
        pass
