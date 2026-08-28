from collections import UserDict
from datetime import datetime, timedelta
from src.models import Name, Phone, Birthday, Email, Address

class Record:
    """Клас для зберігання інформації про контакт (ім'я, телефони, день народження, email, адреса)."""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

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

    def add_email(self, email_str: str):
        """Додає новий email контакту (перезапис заборонено, використовуйте edit_email)."""
        if self.email is not None:
            raise ValueError("Email already exists. Use edit-email to change it.")
        self.email = Email(email_str)

    def edit_email(self, new_email_str: str):
        """Змінює (або встановлює) email контакту."""
        self.email = Email(new_email_str)

    def add_address(self, address_str: str):
        """Додає або оновлює текстову адресу контакту."""
        self.address = Address(address_str)

    def __str__(self):
        bday_str = f", birthday: {self.birthday}" if self.birthday else ""
        email_str = f", email: {self.email}" if self.email else ""
        address_str = f", address: {self.address}" if self.address else ""
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(p.value for p in self.phones)}"
            f"{bday_str}{email_str}{address_str}"
        )

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

    def get_upcoming_birthdays(self, days: int = 7) -> list:
        """Повертає список контактів, яких потрібно привітати протягом наступних `days` днів."""
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

            # Перевіряємо інтервал від 0 до `days` днів включно
            days_until = (bday_this_year - today).days
            if 0 <= days_until <= days:
                congratulation_date = bday_this_year
                # Якщо припадає на вихідні (Субота = 5, Неділя = 6), переносимо на Понеділок
                if bday_this_year.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif bday_this_year.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays

    def search(self, query: str) -> list:
        """Шукає контакти, у яких ім'я, телефон, email або адреса містять підрядок query (без урахування регістру)."""
        if not query:
            return []

        query_lower = query.lower()
        results = []

        for record in self.data.values():
            haystacks = [record.name.value]
            haystacks.extend(phone.value for phone in record.phones)
            if record.email:
                haystacks.append(record.email.value)
            if record.address:
                haystacks.append(record.address.value)

            if any(query_lower in haystack.lower() for haystack in haystacks):
                results.append(record)

        return results
