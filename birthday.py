from datetime import datetime
from fields_interface import Field, Validate


class Birthday(Field, Validate):
    def __init__(self, value):
        self._validate(value)
        super().__init__(value)

    def _validate(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self._value
