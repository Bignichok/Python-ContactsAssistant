"""Handler module"""

from contactcompleter import ContactCompleter
from constants import GREETING_BANNER
from menu import Menu
from utils import format_greeting
from dataHelpers import save_data, load_data
from contactsBook import ContactsBook
from Record import Record

NOT_FOUND_MESSAGE = "Contact does not exist, you can add it"


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


class Handler:
    """Class"""

    def __init__(self) -> None:
        self.contact_book = load_data()
        if not self.contact_book:
            self.contact_book = ContactsBook()
        self.completer = ContactCompleter(Menu.get_commands_witn_args(), self.contact_book)

    def greeting(self) -> str:
        """Print greeting message"""
        res = f"{format_greeting(GREETING_BANNER)}\n"
        res += f"Welcome to the assistant bot!\n{Menu.pretty_print()}"
        return res

    def hello(self, args: list = None) -> str:
        """Print hello message"""
        return f"How can I help you? \n{Menu.pretty_print()}"

    @handle_error
    def add_contact(self, args):
        """
        Add a contact to the address book or update an existing contact.

        Args:
            args (list): List containing name and phone number.
            book (AddressBook): The address book to add the contact to.

        Returns:
            str: Message indicating whether the contact was added or updated.
        """
        name, phone, *_ = args
        record = self.contact_book.find_by_name(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            self.contact_book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        if len(args) > 2:
            record.add_email(args[2])
        return message

    @handle_error
    def update_contact(self, args):
        """
        Change the phone number of an existing contact.

        Args:
            args (list): List containing name, old phone number, and new phone number.
            book (AddressBook): The address book containing the contact.

        Returns:
            str: Message indicating whether the phone number was changed or if the contact was not found.
        """
        name, old_number, new_number = args
        record = self.contact_book.find_by_name(name)
        if record is None:
            return NOT_FOUND_MESSAGE
        record.edit_phone(old_number, new_number)
        return "Phone changed"

    @handle_error
    def delete_contact(self, args):
        """
        Removes an contact from address book.

        Args:
            args (list): List containing contact name.
            book (AddressBook): The address book.

        Returns:
            str: Message indicating whether the contact was added or updated.
        """
        name = args[0]
        if self.contact_book.delete(name) is None:
            return f"Contact with name {name} does not exist."
        return "Contact removed."

    @handle_error
    def set_contact_birthday(self, args):
        """
        Add a birthday to a contact.

        Args:
            args (list): List containing name and birthday date.
            book (AddressBook): The address book containing the contact.

        Returns:
            str: Message indicating whether the birthday was added or if the contact was not found.
        """
        name, date = args
        record = self.contact_book.find_by_name(name)
        if record:
            record.add_birthday(date)
            return "Birthday added."
        return NOT_FOUND_MESSAGE

    @handle_error
    def get_contact_birthday(self, args):
        """
        Show the birthday of a contact.

        Args:
            args (list): List containing the name of the contact.
            book (AddressBook): The address book containing the contact.

        Returns:
            str: The birthday date or a message indicating the birthday was not added or the contact was not found.
        """

        if len(args) < 1:
            return "Provide contact name please"
        name = args[0]
        record = self.contact_book.find_by_name(name)
        if record:
            if record.birthday:
                return record.birthday
            else:
                return "Birthday not added to this contact."
        else:
            return NOT_FOUND_MESSAGE

    @handle_error
    def get_upcoming_birthdays(self, args):
        """
        Show all birthdays this week.

        Args:
            args (list): Empty param list.

        Returns:
            list: All upcoming birthdays.
        """
        return self.contact_book.get_upcoming_birthdays()

    @handle_error
    def update_contact_email(self, args) -> str:
        """
        Update contact e-mail

        Args:
            args (list): List containing name, new e-mail of the contact.

        Returns:
            str: Message indicating whether the contact e-mail was updated.
        """
        name, email = args
        record = self.contact_book.find_by_name(name)
        if record is None:
            return NOT_FOUND_MESSAGE
        else:
            record.add_email(email)
            return "Email changed"

    @handle_error
    def get_contact(self, args):
        """
        Show the phone number of a contact.

        Args:
            args (list): List containing the name of the contact.

        Returns:
            str or Record: The contact's record or a message indicating the contact was not found.
        """
        if len(args) < 1:
            return "Provide contact name please"
        name = args[0]
        record = self.contact_book.find_by_name(name)
        if record is None:
            return NOT_FOUND_MESSAGE
        return record

    @handle_error
    def get_contact_by_name(self, args, book: ContactsBook):
        return self.contact_book.get_contact(args, book, "name")

    @handle_error
    def get_contact_by_phone(self, args, book: ContactsBook):
        return self.contact_book.get_contact(args, book, "phone")

    @handle_error
    def get_contact_by_email(self, args, book: ContactsBook):
        return self.contact_book.get_contact(args, book, "email")

    def close(self, args) -> str:
        """Print hello message"""
        save_data(self.contact_book)
        return print("Good bye!")

    def compliance_list(self) -> dict:
        """Return fuction list"""
        return {
            Menu.HELLO: self.hello,
            Menu.ADD_CONTACT: self.add_contact,
            Menu.UPDATE_CONTACT: self.update_contact,
            Menu.DELETE_CONTACT: self.delete_contact,
            Menu.SET_CONTACT_BIRTHDAY: self.set_contact_birthday,
            Menu.GET_CONTACT_BIRTHDAY: self.get_contact_birthday,
            Menu.GET_CONTACT_BY_NAME: self.get_contact,
            Menu.GET_ALL_CONTACTS: None,
            Menu.GET_UPCOMING_BIRTHDAYS: self.get_upcoming_birthdays,
            Menu.UPDATE_CONTACT_EMAIL: self.update_contact_email,
            Menu.NOTE_ADD: None,
            Menu.NOTE_DEL: None,
            Menu.NOTE_TAG: None,
            Menu.NOTE_TAG_DEL: None,
            Menu.NOTE_ALL: None,
            Menu.EXIT: self.close,
            Menu.CLOSE: self.close,
        }

    @handle_error
    def execute(self, command, args: list) -> str:
        """
        Execute the function corresponding the command.

        Args:
            command (Menu): Input command.
            args (list): List of the input params.

        Returns:
            str: Result message of the handle function execution.
        """
        if command is None:
            return "Invalid command."
        Menu.check_params(command, args)
        return self.compliance_list().get(command)(args)
