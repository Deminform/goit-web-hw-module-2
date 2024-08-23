from adress_book import AddressBook
import pickle
from abc import ABC, abstractmethod


class BaseFileManager(ABC):
    @staticmethod
    @abstractmethod
    def save(book, file_path):
        pass

    @staticmethod
    @abstractmethod
    def load(file_path):
        pass


class PickleFileManager(BaseFileManager):

    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, book: AddressBook):
        with open(self.file_path, "wb") as file:
            pickle.dump(book, file)

    def load(self) -> AddressBook:
        with open(self.file_path, "rb") as file:
            return pickle.load(file)
