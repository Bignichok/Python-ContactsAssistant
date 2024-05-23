"""Main App"""

from contactsBook import ContactsBook
from constants import INPUT_STYLE
from handler import Handler
from menu import Menu
from Record import Record
from dataHelpers import save_data, load_data
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

not_found_message = "Contact does not exist, you can add it"

handler = Handler()


def handle_error(func):
    """
    Decorator to handle exceptions in the wrapped function.

    Args:
        func (function): The function to wrap with error handling.

    Returns:
        function: The wrapped function with error handling.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return str(error)

    return inner


@handle_error
def add_contact(args, book: ContactsBook):
    """
    Add a contact to the address book or update an existing contact.

    Args:
        args (list): List containing name and phone number.
        book (ContactsBook): The address book to add the contact to.

    Returns:
        str: Message indicating whether the contact was added or updated.
    """
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    if len(args) > 2:
        record.add_email(args[2])
    return message


@handle_error
def delete_contact(args, book: ContactsBook):
    """
    Removes an contact from address book.

    Args:
        args (list): List containing contact name.
        book (ContactsBook): The address book.

    Returns:
        str: Message indicating whether the contact was added or updated.
    """
    name = args[0]
    if book.delete(name) is None:
        return f"Contact with name {name} does not exist."
    return "Contact removed."


@handle_error
def change_contact(args, book: ContactsBook):
    """
    Change the phone number of an existing contact.

    Args:
        args (list): List containing name, old phone number, and new phone number.
        book (ContactsBook): The address book containing the contact.

    Returns:
        str: Message indicating whether the phone number was changed or if the contact was not found.
    """
    name, old_number, new_number = args
    record = book.find(name)
    if record is None:
        return not_found_message
    else:
        record.edit_phone(old_number, new_number)
        return "Phone changed"


@handle_error
def update_contact_email(args, book: ContactsBook):
    name, email = args
    record = book.find(name)
    if record is None:
        return not_found_message
    else:
        record.add_email(email)
        return "Email changed"


@handle_error
def get_contact(args, book: ContactsBook, search_by: str):
    """
    Show the contact's record based on the search criteria.

    Args:
        args (list): List containing the search term (name, phone, or email).
        book (ContactsBook): The address book containing the contact.
        search_by (str): The type of search ('name', 'phone', 'email').

    Returns:
        str or Record: The contact's record or a message indicating the contact was not found.
    """
    if len(args) < 1:
        return f"Provide contact {search_by} please"

    search_term = args[0]

    if search_by == "name":
        record = book.find_by_name(search_term)
    elif search_by == "phone":
        record = book.find_by_phone(search_term)
    elif search_by == "email":
        record = book.find_by_email(search_term)
    else:
        return "Invalid search type specified"

    if record is None:
        return "Contact not found"
    return record


@handle_error
def get_contact_by_name(args, book: ContactsBook):
    return get_contact(args, book, "name")


@handle_error
def get_contact_by_phone(args, book: ContactsBook):
    return get_contact(args, book, "phone")


@handle_error
def get_contact_by_email(args, book: ContactsBook):
    return get_contact(args, book, "email")


@handle_error
def set_contact_birthday(args, book: ContactsBook):
    """
    Add a birthday to a contact.

    Args:
        args (list): List containing name and birthday date.
        book (ContactsBook): The address book containing the contact.

    Returns:
        str: Message indicating whether the birthday was added or if the contact was not found.
    """
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added."
    else:
        return not_found_message


@handle_error
def get_contact_birthday(args, book: ContactsBook):
    """
    Show the birthday of a contact.

    Args:
        args (list): List containing the name of the contact.
        book (ContactsBook): The address book containing the contact.

    Returns:
        str: The birthday date or a message indicating the birthday was not added or the contact was not found.
    """

    if len(args) < 1:
        return "Provide contact name please"
    name = args[0]

    record = book.find(name)
    if record:
        if record.birthday:
            return record.birthday
        else:
            return "Birthday not added to this contact."
    else:
        return not_found_message


def parse_input(user_input):
    """
    Parse user input into a command and its arguments.

    Args:
        user_input (str): The input string from the user.

    Returns:
        tuple: The command and a list of arguments.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    """
    Main function to run the assistant bot.

    Continuously prompts the user for commands and executes the appropriate function.
    """
    book = load_data()
    print(handler.greeting())
    while True:
        style = Style.from_dict(INPUT_STYLE)
        completer = WordCompleter(Menu.get_commands_list())
        user_input = prompt("Enter a command >>> ", completer=completer, style=style)
        print()

        command, *args = parse_input(user_input)

        match command:
            case "hello":
                print(handler.hello())
            case "close" | "exit":
                save_data(book)
                print("Good bye!")
                break
            case "add_contact":
                print(add_contact(args, book))
            case "update_contact":
                print(change_contact(args, book))
            case "delete_contact":
                print(delete_contact(args, book))
            case "set_contact_birthday":
                print(set_contact_birthday(args, book))
            case "get_contact_birthday":
                print(get_contact_birthday(args, book))
            case "get_contact_by_name":
                print(get_contact_by_name(args, book))
            case "get_contact_by_phone":
                print(get_contact_by_phone(args, book))
            case "get_contact_by_email":
                print(get_contact_by_email(args, book))
            case "get_all_contacts":
                print(book)
            case "get_upcoming_birthdays":
                print(book.get_upcoming_birthdays())
            case "update_contact_email":
                print(update_contact_email(args, book))
            case "help":
                print("Allowed commands:")
                print(Menu.get_commands_list())
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()
