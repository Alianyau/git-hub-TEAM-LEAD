import difflib
from src.storage import save_data, load_data
from src.handlers import (
    parse_input,
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
    add_email,
    edit_email,
    add_address,
    search_contacts,
    delete_contact,
    add_note,
    add_tag,
    search_notes,
    search_by_tag,
    show_all_notes,
    delete_note
)

# Список усіх команд для розумних автопідказок
COMMANDS = [
    "hello", "add", "change", "phone", "all", "delete",
    "add-birthday", "show-birthday", "birthdays",
    "add-email", "edit-email", "add-address", "search",
    "add-note", "add-tag", "search-notes", "search-by-tag", "all-notes", "delete-note",
    "close", "exit"
]

def suggest_command(user_command):
    """Шукає найближчу за написанням команду при помилці вводу."""
    matches = difflib.get_close_matches(user_command, COMMANDS, n=1, cutoff=0.5)
    return matches[0] if matches else None

def main():
    # Завантажуємо стан адресної книги та нотаток з файлів
    book, notebook = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if not command:
            continue

        if command in ["close", "exit"]:
            # Зберігаємо стан перед виходом
            save_data(book, notebook)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        # --- Команди адресної книги ---
        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "delete":
            print(delete_contact(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        elif command == "add-email":
            print(add_email(args, book))

        elif command == "edit-email":
            print(edit_email(args, book))

        elif command == "add-address":
            print(add_address(args, book))

        elif command == "search":
            print(search_contacts(args, book))

        # --- Команди нотаток ---
        elif command == "add-note":
            print(add_note(args, notebook))

        elif command == "add-tag":
            print(add_tag(args, notebook))

        elif command == "search-notes":
            print(search_notes(args, notebook))

        elif command == "search-by-tag":
            print(search_by_tag(args, notebook))

        elif command == "all-notes":
            print(show_all_notes(notebook))

        elif command == "delete-note":
            print(delete_note(args, notebook))

        else:
            # Інтелектуальний аналіз: пропонуємо схожу команду
            closest = suggest_command(command)
            if closest:
                print(f"Invalid command. Did you mean '{closest}'?")
            else:
                print("Invalid command.")

if __name__ == "__main__":
    main()