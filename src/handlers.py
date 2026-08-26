from src.decorators import input_error
from src.address_book import AddressBook, Record

def parse_input(user_input):
    """Розбирає введений рядок на команду та аргументи."""
    parts = user_input.split()
    if not parts:
        return "", []
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args

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
    if len(args) < 2:
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
    """Показує дні народження на найближчий тиждень."""
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next week."
    
    result = []
    for item in upcoming:
        result.append(f"{item['name']}: {item['congratulation_date']}")
    return "\n".join(result)