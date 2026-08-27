import pickle
from src.address_book import AddressBook


def save_data(book, notebook=None, filename_book="data/addressbook.pkl", filename_note="data/notebook.pkl"):
    """Зберігає об'єкти AddressBook та NoteBook у відповідні файли pickle."""
    with open(filename_book, "wb") as f:
        pickle.dump(book, f)

    if notebook is not None:
        with open(filename_note, "wb") as f:
            pickle.dump(notebook, f)


def load_data(filename_book="data/addressbook.pkl", filename_note="data/notebook.pkl"):
    """Завантажує AddressBook та NoteBook з файлів або повертає нові об'єкти."""
    try:
        with open(filename_book, "rb") as f:
            book = pickle.load(f)
    except FileNotFoundError:
        book = AddressBook()

    notebook = None
    try:
        # Динамічний імпорт NoteBook (якщо клас уже створено в note_book.py)
        from src.note_book import NoteBook
        try:
            with open(filename_note, "rb") as f:
                notebook = pickle.load(f)
        except FileNotFoundError:
            notebook = NoteBook()
    except (ImportError, Exception):
        # Якщо NoteBook ще в розробці — пропускаємо без помилок
        pass

    return book, notebook