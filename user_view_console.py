import pickle

from colorama import Fore, init

from adress_book import AddressBook
from error_decorator import error_decorator
from record import Record

init(autoreset=True)

commands_dict = {
    "hi, hello": "Привітатися з програмою",
    "close, exit": "Вийти з програми",
    "all": "Показати всі доступні записи",
    "add": "Додати новий запис",
    "delete": "Видалити існуючий запис",
    "change": "Змінити існуючий запис",
    "phone": "Показати телефонні номери для контакту",
    "add-birthday": "Додати дату народження для контакту",
    "show-birthday": "Показати дату народження контакту",
    "birthdays": "Показати найближчі дні народження всіх контактів",
}


@error_decorator
def main():
    book = load_data()
    print("------------------------------------------------------------------------------------\n"
          "--------------------------- Welcome to the assistant bot! --------------------------\n"
          "-h or -help for info")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("------------------------------------------------------------------------------------\n"
                  "---------------------------- All the data has been saved. --------------------------\n"
                  "------------------------------------- Good bye! ------------------------------------")
            break

        elif command in ["-h", "-help"]:
            max_len = max(len(key) for key in commands_dict.keys())
            for key, value in commands_dict.items():
                print(f"{key.ljust(max_len)}   {value}")

        elif command in ["hi", "hello"]:
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "delete":
            print(delete(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(book)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(book.get_upcoming_birthdays())

        else:
            print(Fore.YELLOW + "Invalid command.")


@error_decorator
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@error_decorator
def add_contact(args: list, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated"
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        message = "Contact added"
        return message
    elif phone:
        record.add_phone(phone)
    return message


@error_decorator
def delete(args: list, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is not None:
        book.delete(name)
        return "Contact deleted"
    return "Contact not found"


@error_decorator
def change_phone(args: list, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return f"Phone changed from {old_phone} to {new_phone} for contact: {record.name.value}"


@error_decorator
def show_phone(args: list, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError(f'Record with name: "{name}" does not exist')
    return record.show_phones()


@error_decorator
def add_birthday(args: list, book: AddressBook):
    name, date_of_birth, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError(f"Record with name: {name} does not exist")

    if record.birthday is None:
        record.add_birthday(date_of_birth)
    else:
        raise ValueError(f"Record with name: {record.name.value} already has birthday")

    return "Birthday added"


@error_decorator
def show_birthday(args: list, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError(f"Record with name: {name} does not exist")
    return record.show_birthday()


@error_decorator
def save_data(book, filename="files/new_addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


@error_decorator
def load_data(filename="files/new_addressbook.pkl"):
    with open(filename, "rb") as file:
        return pickle.load(file)


if __name__ == "__main__":
    main()
