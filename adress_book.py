from collections import UserDict
from datetime import date, timedelta, datetime

from record import Record
from prettytable import PrettyTable


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return next((record for record in self.data.values() if str(record.name.value).lower() == name.lower()), None)

    def delete(self, name: str):
        for contact in self.data.keys():
            if contact.lower() == name.lower():
                del self.data[contact]
                break

    @staticmethod
    def string_to_date(date_string) -> date:
        return datetime.strptime(date_string, '%d.%m.%Y').date()

    @staticmethod
    def date_to_string(value):
        return value.strftime('%d.%m.%Y')

    @staticmethod
    def find_next_weekday(start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7) -> str:
        """
        Retrieve from a list of entries with birthdays in the next 7 days.
        The result is returned as a table.
        """
        upcoming_birthdays = []
        today = date.today()

        for record in self.data.values():
            if record.birthday is not None:
                date_of_birth = self.string_to_date(record.birthday.value).replace(year=today.year)

                if date_of_birth < today:
                    date_of_birth = self.string_to_date(record.birthday.value).replace(year=today.year + 1)

                if 0 <= (date_of_birth - today).days <= days:
                    birthday_this_year = self.adjust_for_weekend(date_of_birth)

                    congratulation_date_str = self.date_to_string(birthday_this_year)
                    upcoming_birthdays.append({
                        'name': record.name.value,
                        'congratulation_date': congratulation_date_str
                    })

        # Generating a table for return
        table = PrettyTable()
        table.align = 'l'
        table.field_names = ['#', '-- Name --', '-- Congratulation date --']

        for index, record in enumerate(upcoming_birthdays, start=1):
            table.add_row([index, record['name'], record['congratulation_date']])

        return table.get_string()

    def __str__(self):
        table = PrettyTable()
        table.align = 'l'
        table.field_names = ['#', '-- Name --', '-- Phones --', '-- Birthday --']

        for index, record in enumerate(self.data.values(), start=1):
            phones = ", ".join(phone.value for phone in record.phones)
            table.add_row([index, record.name.value, phones, record.birthday])

        return table.get_string()
