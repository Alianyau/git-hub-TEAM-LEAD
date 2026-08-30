import os
import pickle
from src.address_book import AddressBook
from src.note_book import NoteBook


def save_data(book: AddressBook, notebook: NoteBook = None, filename_book="data/addressbook.pkl", filename_note="data/notebook.pkl"):
    """Зберігає об'єкти AddressBook та NoteBook у відповідні файли pickle."""
    os.makedirs(os.path.dirname(filename_book), exist_ok=True)
    with open(filename_book, "wb") as f:
        pickle.dump(book, f)

    if notebook is not None:
        os.makedirs(os.path.dirname(filename_note), exist_ok=True)
        with open(filename_note, "wb") as f:
            pickle.dump(notebook, f)


def load_data(filename_book="data/addressbook.pkl", filename_note="data/notebook.pkl"):
    """Завантажує AddressBook та NoteBook з файлів або повертає нові об'єкти."""
    try:
        with open(filename_book, "rb") as f:
            book = pickle.load(f)
    except (FileNotFoundError, Exception):
        book = AddressBook()

    try:
        with open(filename_note, "rb") as f:
            notebook = pickle.load(f)
    except (FileNotFoundError, Exception):
        notebook = NoteBook()

    return book, notebook