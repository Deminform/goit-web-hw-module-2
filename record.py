from birthday import Birthday
from name import Name
from phone import Phone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # @input_error
    def add_birthday(self, value: str):
        self.birthday = Birthday(value)

    def show_birthday(self):
        return self.birthday.value

    def add_phone(self, phone_number: str):
        if next(
            (phone.value for phone in self.phones if phone.value == phone_number), None
        ):
            raise ValueError(f"Phone number {phone_number} already exists")
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)

    def edit_phone(self, phone_number: str, new_phone_number: str):
        if not self.find_phone(phone_number):
            raise ValueError(f"Phone number {phone_number} does not exist")
        self.add_phone(new_phone_number)
        self.remove_phone(phone_number)

    def show_phones(self):
        return "; ".join(phone.value for phone in self.phones)

    def find_phone(self, phone_number: str):
        return next(
            (phone for phone in self.phones if phone.value == phone_number), None
        )

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(phone.value for phone in self.phones)}"
