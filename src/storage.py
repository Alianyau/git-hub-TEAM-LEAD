import pickle
from src.address_book import AddressBook

def save_data(book, filename="data/addressbook.pkl"):
    """Зберігає об'єкт AddressBook у файл за допомогою pickle."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="data/addressbook.pkl"):
    """Завантажує AddressBook з файлу або створює новий об'єкт, якщо файл відсутній."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()