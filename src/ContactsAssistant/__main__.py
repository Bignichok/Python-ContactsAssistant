from AddressBook import AddressBook
from Record import Record
from dataHelpers import save_data, load_data

not_found_message = "Contact does not exist, you can add it"

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
def add_contact(args, book: AddressBook):
    """
    Add a contact to the address book or update an existing contact.

    Args:
        args (list): List containing name and phone number.
        book (AddressBook): The address book to add the contact to.

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
    return message

@handle_error
def change_contact(args, book: AddressBook):
    """
    Change the phone number of an existing contact.

    Args:
        args (list): List containing name, old phone number, and new phone number.
        book (AddressBook): The address book containing the contact.

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
def show_phone(args, book: AddressBook):
    """
    Show the phone number of a contact.

    Args:
        args (list): List containing the name of the contact.
        book (AddressBook): The address book containing the contact.

    Returns:
        str or Record: The contact's record or a message indicating the contact was not found.
    """
    name = args[0]
    record = book.find(name)
    if record is None:
        return not_found_message
    return record

@handle_error
def add_birthday(args, book: AddressBook):
    """
    Add a birthday to a contact.

    Args:
        args (list): List containing name and birthday date.
        book (AddressBook): The address book containing the contact.

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
def show_birthday(args, book: AddressBook):
    """
    Show the birthday of a contact.

    Args:
        args (list): List containing the name of the contact.
        book (AddressBook): The address book containing the contact.

    Returns:
        str: The birthday date or a message indicating the birthday was not added or the contact was not found.
    """
    name = args[0]
    record = book.find(name)
    if record:
        if record.birthday:
            return record.birthday
        else:
            return 'Birthday not added to this contact.'
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
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        
        match command:
            case "hello":
                print("How can I help you?")
            case "close" | "exit":
                save_data(book)
                print("Good bye!")
                break
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                print(book)
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(book.get_upcoming_birthdays())
            case _:
                print("Invalid command.")

if __name__ == "__main__":
    main()
