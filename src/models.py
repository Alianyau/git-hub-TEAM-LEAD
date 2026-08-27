import re
from datetime import datetime


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


class Email(Field):
    """Клас для зберігання email з валідацією через regex."""
    def __init__(self, value: str):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format.")
        super().__init__(value)


class Address(Field):
    """Клас для зберігання текстової адреси контакту."""
    pass


class Note:
    """Клас для зберігання нотатки (текст, теги)."""
    def __init__(self, content: str, tags: list = None):
        self.content = content
        self.tags = tags if tags else []

    def add_tag(self, tag: str):
        """Додає новий тег до нотатки."""
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        """Видаляє тег з нотатки."""
        if tag in self.tags:
            self.tags.remove(tag)

    def __str__(self):
        tags_str = f" [Tags: {', '.join(self.tags)}]" if self.tags else ""
        return f"{self.content}{tags_str}"