from functools import wraps

from colorama import Fore, init

from adress_book import AddressBook

init(autoreset=True)


def error_decorator(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return (
                Fore.YELLOW + e.args[0]
                if not e.args[0].startswith("not")
                else "Enter the argument for the command."
            )
        except KeyError:
            return "KeyError."
        except IndexError as e:
            return (
                Fore.YELLOW + e.args[0]
                if not e.args[0].startswith("list")
                else "Enter the argument for the command"
            )
        except FileNotFoundError as e:
            return AddressBook()

    return inner
