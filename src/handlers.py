from src.decorators import input_error
from src.address_book import AddressBook, Record
from src.note_book import NoteBook
from src.models import Note


def parse_input(user_input):
    """Розбирає введений рядок на команду та аргументи."""
    parts = user_input.split()
    if not parts:
        return "", []
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args


# --- ХЕНДЛЕРИ КОНТАКТІВ ---

@input_error
def add_contact(args, book: AddressBook):
    """Додає новий контакт або новий телефон до існуючого контакту."""
    if len(args) < 1:
        raise IndexError
    name = args[0]
    phone = args[1] if len(args) > 1 else None

    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    """Змінює старий телефон контакту на новий."""
    if len(args) < 3:
        raise IndexError
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    """Виводить всі номери телефонів для вказаного контакту."""
    if not args:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.phones:
        return f"No phones saved for {name}."
    return f"{record.name.value}: {'; '.join(p.value for p in record.phones)}"


@input_error
def show_all(book: AddressBook):
    """Виводить усі контакти в адресній книзі."""
    if not book.data:
        return "No contacts saved."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    """Додає день народження до контакту."""
    if len(args) < 2:
        raise IndexError
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday_str)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    """Показує день народження контакту."""
    if not args:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return f"No birthday set for {name}."
    return f"{record.name.value}'s birthday: {record.birthday}"


@input_error
def birthdays(args, book: AddressBook):
    """Показує дні народження на найближчі N днів (за замовчуванням 7)."""
    days = 7
    if args:
        if not args[0].isdigit():
            raise ValueError("Days must be a positive integer.")
        days = int(args[0])

    upcoming = book.get_upcoming_birthdays(days=days)
    if not upcoming:
        return f"No upcoming birthdays in the next {days} days."

    result = []
    for item in upcoming:
        result.append(f"{item['name']}: {item['congratulation_date']}")
    return "\n".join(result)


@input_error
def add_email(args, book: AddressBook):
    """Додає email до контакту."""
    if len(args) < 2:
        raise IndexError
    name, email_str, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_email(email_str)
    return "Email added."


@input_error
def edit_email(args, book: AddressBook):
    """Змінює email контакту."""
    if len(args) < 2:
        raise IndexError
    name, email_str, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_email(email_str)
    return "Email updated."


@input_error
def add_address(args, book: AddressBook):
    """Додає або оновлює адресу контакту."""
    if len(args) < 2:
        raise IndexError
    name = args[0]
    address_str = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_address(address_str)
    return "Address added."


@input_error
def search_contacts(args, book: AddressBook):
    """Шукає контакти за підрядком у імені, телефоні, email або адресі."""
    if not args:
        raise IndexError
    query = " ".join(args)
    results = book.search(query)
    if not results:
        return "No contacts found."
    return "\n".join(str(record) for record in results)


# --- ХЕНДЛЕРИ НОТАТОК ---

@input_error
def add_note(args, notebook: NoteBook):
    """Створює нову нотатку."""
    if not args:
        raise IndexError
    content = " ".join(args)
    notebook.add_note(Note(content))
    return "Note added."


@input_error
def add_tag(args, notebook: NoteBook):
    """Додає тег до нотатки. Формат: <текст_нотатки> <тег>"""
    if len(args) < 2:
        raise IndexError
    tag = args[-1]
    content = " ".join(args[:-1])
    note = notebook.find_note(content)
    if not note:
        raise KeyError
    note.add_tag(tag)
    return f"Tag '{tag}' added to note."


@input_error
def search_notes(args, notebook: NoteBook):
    """Шукає нотатки за текстом."""
    if not args:
        raise IndexError
    query = " ".join(args)
    results = notebook.search_by_text(query)
    if not results:
        return "No notes found."
    return "\n---\n".join(str(n) for n in results)


@input_error
def search_by_tag(args, notebook: NoteBook):
    """Шукає нотатки за тегом."""
    if not args:
        raise IndexError
    tag = args[0]
    results = notebook.search_by_tag(tag)
    if not results:
        return f"No notes found with tag '{tag}'."
    return "\n---\n".join(str(n) for n in results)


@input_error
def show_all_notes(notebook: NoteBook):
    """Виводить усі збережені нотатки."""
    if not notebook.data:
        return "No notes saved."
    return "\n---\n".join(str(note) for note in notebook.data.values())
