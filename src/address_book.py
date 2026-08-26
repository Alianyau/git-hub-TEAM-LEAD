from collections import UserDict
from datetime import datetime, timedelta
from src.models import Name, Phone, Birthday

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
            # Беремо день народження у поточному році
            bday_this_year = bday.replace(year=today.year)

            # Якщо день народження вже минув у цьому році, розглядаємо наступний рік
            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)

            # Перевіряємо інтервал від 0 до 7 днів включно
            days_until = (bday_this_year - today).days
            if 0 <= days_until <= 7:
                congratulation_date = bday_this_year
                # Якщо припадає на вихідні (Субота = 5, Неділя = 6), переношуємо на Понеділок
                if bday_this_year.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif bday_this_year.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays