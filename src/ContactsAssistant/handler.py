"""Handler module"""

from address import AddressType
from command_completer import CommandCompleter
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

    @staticmethod
    def strip_quotes(value):
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            return value[1:-1]
        return value

    def __init__(self) -> None:
        self.contact_book = load_data()
        if not self.contact_book:
            self.contact_book = ContactsBook()
        self.completer = CommandCompleter(
            Menu.get_commands_witn_args(), self.contact_book
        )

    def greeting(self) -> str:
        """Print greeting message"""
        res = f"{format_greeting(GREETING_BANNER)}\n"
        res += f"Welcome to the assistant bot!\n{Menu.pretty_print()}"
        return res

    def hello(self) -> str:
        """Print hello message"""
        return f"How can I help you? \n{Menu.pretty_print()}"

    @handle_error
    def add_contact(self, args):
        """
        Add a contact to the address book or update an existing contact.

        Args:
            args (Namespace): Namespace containing name and phone number.
            book (ContactsBook): The address book to add the contact to.

        Returns:
            str: Message indicating whether the contact was added or updated.
        """

        name = args.name
        phone = args.phone
        email = args.email
        birthday = args.birthday

        record = self.contact_book.find_by_name(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            self.contact_book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        if email:
            record.add_email(email)
        if birthday:
            record.add_birthday(birthday)

        return message

    @handle_error
    def update_contact(self, args):
        """
        Change the phone number of an existing contact.

        Args:
            args (Namespace): Namespace containing name, old phone number, and new phone number.
            book (ContactsBook): The address book containing the contact.

        Returns:
            str: Message indicating whether the phone number was changed or if the contact was not found.
        """
        name = args.name
        old_phone = args.oldphone
        new_phone = args.newphone

        record = self.contact_book.find_by_name(name)
        if record is None:
            return NOT_FOUND_MESSAGE
        record.edit_phone(old_phone, new_phone)
        return "Phone changed"

    @handle_error
    def delete_contact(self, args):
        """
        Removes an contact from address book.

        Args:
            args (Namespace): Namespace containing contact name.
            book (ContactsBook): The address book.

        Returns:
            str: Message indicating whether the contact was added or updated.
        """
        name = args.name
        if self.contact_book.delete(name) is None:
            return f"Contact with name {name} does not exist."
        return "Contact removed."

    @handle_error
    def set_contact_birthday(self, args):
        """
        Add a birthday to a contact.

        Args:
            args (Namespace): Namespace containing name and birthday date.
            book (ContactsBook): The address book containing the contact.

        Returns:
            str: Message indicating whether the birthday was added or if the contact was not found.
        """
        name = args.name
        birthday = args.birthday
        record = self.contact_book.find_by_name(name)
        if record:
            record.add_birthday(birthday)
            return "Birthday added."
        return NOT_FOUND_MESSAGE

    @handle_error
    def get_contact_birthday(self, args):
        """
        Show the birthday of a contact.

        Args:
            args (Namespace): Namespace containing the name of the contact.
            book (ContactsBook): The address book containing the contact.

        Returns:
            str: The birthday date or a message indicating the birthday was not added or the contact was not found.
        """

        name = args.name
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
            args (list):

        Returns:
            list: All upcoming birthdays.
        """
        days = args.days
        if days:
            return self.contact_book.get_upcoming_birthdays(int(days)).__str__()
        else:
            return self.contact_book.get_upcoming_birthdays().__str__()

    @handle_error
    def update_contact_email(self, args) -> str:
        """
        Update contact e-mail

        Args:
            args (Namespace): Namespace containing name, new e-mail of the contact.

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
    def add_address(self, args):
        """
        add or update address of contact.

        Args:
            args (Namespace): Namespace containing contact name.
            book (ContactsBook): The address book.

        Returns:
            str: Message indicating whether the contact was added or updated.
        """
        name = args.name
        address_type = args.addresstype

        address_type = AddressType(address_type)

        street = args.street
        city = args.city
        postalcode = args.postalcode
        country = args.country
        record = self.contact_book.find_by_name(name)
        if record is None:
            return NOT_FOUND_MESSAGE
        if address_type in record.addresses:
            record.edit_address(address_type, street, city, postalcode, country)
            return "Address updated."
        else:
            record.add_address(address_type, street, city, postalcode, country)

        return "Address added."

    @handle_error
    def remove_address(self, args):
        """
        Removes an contact address from contact.

        Args:
            args (Namespace): Namespace containing contact name.
            book (ContactsBook): The address book.

        Returns:
            str: Message indicating whether the address deleted.
        """
        name = args.name
        address_type = args.addresstype

        address_type = AddressType(address_type)

        record = self.contact_book.find_by_name(name)
        if record is None:
            return NOT_FOUND_MESSAGE
        if address_type in record.addresses:
            record.remove_address(address_type)
            return "Address removed."

        return "Address not found."

    @handle_error
    def get_contact(self, args):
        """
        Show the phone number of a contact.

        Args:
            args (Namespace): Namespace containing the name of the contact.

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

    def close(self) -> str:
        """return bye message"""
        save_data(self.contact_book)
        return "Good bye!"

    def __compliance_list(self) -> dict:
        """Return fuction list"""
        return {
            Menu.ADD_CONTACT: self.add_contact,
            Menu.UPDATE_CONTACT: self.update_contact,
            Menu.DELETE_CONTACT: self.delete_contact,
            Menu.SET_CONTACT_BIRTHDAY: self.set_contact_birthday,
            Menu.GET_CONTACT_BIRTHDAY: self.get_contact_birthday,
            Menu.GET_CONTACT_BY_NAME: self.get_contact,
            Menu.GET_UPCOMING_BIRTHDAYS: self.get_upcoming_birthdays,
            Menu.UPDATE_CONTACT_EMAIL: self.update_contact_email,
            Menu.ADDRESS: self.add_address,
            Menu.DELETE_ADDRESS: self.remove_address,
            Menu.NOTE_ADD: None,
            Menu.NOTE_DEL: None,
            Menu.NOTE_TAG: None,
            Menu.NOTE_TAG_DEL: None,
            Menu.NOTE_ALL: None,
        }

    def __without_params_commands(self) -> dict:
        """Return fuction list"""
        return {
            Menu.HELLO: self.hello,
            Menu.GET_ALL_CONTACTS: self.contact_book.__str__,
            Menu.EXIT: self.close,
            Menu.CLOSE: self.close,
        }

    @handle_error
    def execute(self, command, args: list) -> str:
        """
        Execute the function corresponding the command.

        Args:
            command (Menu): Input command.
            args (Namespace): Namespace of the input params.

        Returns:
            str: Result message of the handle function execution.
        """
        if command is None:
            return ""

        if command in self.__without_params_commands():
            return self.__without_params_commands().get(command)()
        else:
            return self.__compliance_list().get(command)(args)
