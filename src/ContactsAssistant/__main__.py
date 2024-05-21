from AddressBook import AddressBook
from Record import Record
from dataHelpers import save_data, load_data

not_found_message = "Contact does not exist, you can add it"

def handle_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            return str(error)

    return inner

@handle_error
def add_contact(args, book: AddressBook):
    name, phone, email = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    if email:
        record.add_email(email)
    return message

@handle_error
def change_contact(args, book: AddressBook):
    name, old_number, new_number = args
    record = book.find(name)
    if record is None:
        return not_found_message
    else:
        record.edit_phone(old_number, new_number)
        return "Phone changed"
    
@handle_error
def change_email(args, book: AddressBook):
    name, email = args
    record = book.find(name)
    if record is None:
        return not_found_message
    else:
        record.add_email(email)
        return "Email changed"
    
@handle_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return not_found_message
    return record

@handle_error
def add_birthday(args, book: AddressBook):
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added."
    else:
        return not_found_message

@handle_error
def show_birthday(args, book: AddressBook):
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
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
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
            case "change-email":
                print(change_email(args, book))
            case _:
                print("Invalid command.")

if __name__ == "__main__":
    main()
