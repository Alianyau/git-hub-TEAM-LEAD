class InvalidEmailError(ValueError):
    """Помилка: некоректний формат email."""
    pass


class InvalidTagError(ValueError):
    """Помилка: некоректний або порожній тег нотатки."""
    pass


class NoteNotFoundError(KeyError):
    """Помилка: нотатку за вказаним запитом не знайдено."""
    pass


def input_error(func):
    """Декоратор для перехоплення винятків та виведення зручних повідомлень."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidEmailError as e:
            return str(e) if str(e) else "Invalid email format."
        except InvalidTagError as e:
            return str(e) if str(e) else "Invalid tag. Tag must be a non-empty string."
        except NoteNotFoundError as e:
            return str(e) if str(e) else "Note not found."
        except ValueError as e:
            return str(e) if str(e) else "Give me name and phone/date please."
        except IndexError:
            return "Enter the argument for the command."
        except KeyError:
            return "Contact not found."
        except AttributeError:
            return "Operation not supported for this record."
        except TypeError:
            return "Invalid arguments for the command."
    return inner
