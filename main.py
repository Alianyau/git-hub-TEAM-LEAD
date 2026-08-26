import pickle
from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (10 цифр)."""
    def __init__(self, value: str):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    """Клас для зберігання дня народження з валідацією формату DD.MM.YYYY."""
    def __init__(self, value: str):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Клас для зберігання інформації про контакт (ім'я, телефони, день народження)."""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number: str):
        """Додає новий номер телефону."""
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str):
        """Видаляє номер телефону зі списку."""
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_number: str, new_number: str):
        """Змінює старий номер телефону на новий."""
        phone_obj = self.find_phone(old_number)
        if not phone_obj:
            raise ValueError(f"Phone number {old_number} not found.")
        
        new_phone_obj = Phone(new_number)
        index = self.phones.index(phone_obj)
        self.phones[index] = new_phone_obj

    def find_phone(self, phone_number: str):
        """Шукає та повертає об'єкт Phone за номером."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday_str: str):
        """Додає або перезаписує день народження контакту."""
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        bday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{bday_str}"


class AddressBook(UserDict):
    """Клас для зберігання записів та керування ними."""
    def add_record(self, record: Record):
        """Додає запис до адресної книги."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """Повертає запис за ім'ям (або None, якщо не знайдено)."""
        return self.data.get(name)

    def delete(self, name: str):
        """Видаляє запис з адресної книги."""
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list:
        """Повертає список контактів, яких потрібно привітати протягом наступних 7 днів."""
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.value
            bday_this_year = bday.replace(year=today.year)

            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)

            days_until = (bday_this_year - today).days
            if 0 <= days_until <= 7:
                congratulation_date = bday_this_year
                if bday_this_year.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif bday_this_year.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays


# --- Серіалізація та десеріалізація даних ---

def save_data(book, filename="addressbook.pkl"):
    """Зберігає об'єкт AddressBook у файл за допомогою pickle."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """Завантажує AddressBook з файлу або створює новий об'єкт, якщо файл відсутній."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


# --- Декоратор та хендлери команд ---

def input_error(func):
    """Декоратор для перехоплення винятків та виведення зручних повідомлень."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e) if str(e) else "Give me name and phone/date please."
        except IndexError:
            return "Enter the argument for the command."
        except KeyError:
            return "Contact not found."

    return inner


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


def main():
    # Завантажуємо стан адресної книги з файлу при запуску
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if not command:
            continue

        if command in ["close", "exit"]:
            # Зберігаємо стан адресної книги у файл перед виходом
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()