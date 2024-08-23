from adress_book import AddressBook
from error_decorator import error_decorator
from file_manager import PickleFileManager
from record import Record
from user_view_interface import ContactManager, ContactReader


class UserView(ContactManager, ContactReader):

    def __init__(self, file_path):
        self.file_manager = PickleFileManager(file_path)
        self.book = self.load_data()

    @error_decorator
    def save_data(self):
        self.file_manager.save(self.book)

    @error_decorator
    def load_data(self) -> AddressBook:
        return self.file_manager.load()

    @error_decorator
    def add_contact(self, name, phone_number):
        record = self.book.find(name)
        message = "Contact updated"
        if record is None:
            record = Record(name)
            record.add_phone(phone_number)
            self.book.add_record(record)
            message = "Contact added"
            return message
        else:
            record.add_phone(phone_number)
        return message

    @error_decorator
    def delete_contact(self, name):
        record = self.book.find(name)
        if record:
            self.book.delete(name)
            return f'Contact "{name}" deleted'
        return "Contact not found"

    @error_decorator
    def update_phone(self, name, old_phone, new_phone):
        record = self.book.find(name)
        record.edit_phone(old_phone, new_phone)
        return f"Phone changed from {old_phone} to {new_phone} for contact: {record.name.value}"

    @error_decorator
    def add_birthday(self, name, date_of_birth):
        record = self.book.find(name)
        if record is None:
            raise ValueError(f"Record with name: {name} does not exist")

        if record.birthday is None:
            record.add_birthday(date_of_birth)
        else:
            raise ValueError(
                f"Record with name: {record.name.value} already has birthday"
            )
        return "Birthday added"

    @error_decorator
    def show_contacts(self):
        return self.book

    @error_decorator
    def show_birthday(self, name):
        record = self.book.find(name)
        if record is None:
            raise ValueError(f"Record with name: {name} does not exist")
        return record.show_birthday()

    @error_decorator
    def show_upcoming_birthdays(self):
        return self.book.get_upcoming_birthdays()

    @error_decorator
    def show_phone(self, name):
        record = self.book.find(name)
        if record is None:
            raise ValueError(f'Record with name: "{name}" does not exist')
        return record.show_phones()


if __name__ == "__main__":
    new_user = UserView("files/new_addressbook.pkl")
    print(new_user.add_contact("Lora", "8888888888"))
    print(new_user.add_birthday("Lora", "29.08.2000"))
    print(new_user.show_upcoming_birthdays())
    print(new_user.delete_contact("Lora"))
    print(new_user.show_phone("Lora"))
    print(new_user.show_contacts())
    new_user.save_data()
