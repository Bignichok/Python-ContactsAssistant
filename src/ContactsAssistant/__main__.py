"""Main App"""

from contactsBook import ContactsBook
from constants import INPUT_STYLE
from handler import Handler
from menu import Menu
from Record import Record
from dataHelpers import save_data, load_data
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from contactcompleter import ContactCompleter
from notebook import Notebook
from note import Note


NOT_FOUND_MESSAGE = "Contact does not exist, you can add it"

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
        return NOT_FOUND_MESSAGE
    else:
        record.edit_phone(old_number, new_number)
        return "Phone changed"


@handle_error
def update_contact_email(args, book: ContactsBook):
    name, email = args
    record = book.find(name)
    if record is None:
        return NOT_FOUND_MESSAGE
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
        return NOT_FOUND_MESSAGE


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
        return NOT_FOUND_MESSAGE


@handle_error
def get_upcoming_birthdays(args, book: ContactsBook):
    """
    Show the birthday of a contact.

    Args:
        args (list): List containing the name of the contact.
        book (ContactsBook): The address book containing the contact.

    Returns:
        str: The birthday date or a message indicating the birthday was not added or the contact was not found.
    """
    if len(args) > 0:
        days = args[0]

    if days:
        return book.get_upcoming_birthdays(int(days))
    else:
        return book.get_upcoming_birthdays()


@handle_error
def add_note_prompt(args, notebook: Notebook):
    """
    Add a note to the notebook via user prompt.

    Args:
        args (list): List of arguments.
        notebook (Notebook): The notebook to add the note to.

    Returns:
        str: Message indicating whether the note was added or not.
    """
    title = input("Enter title: ")
    content = input("Enter content: ")
    tags = input("Enter tags (comma-separated): ").split(",")
    due_date = input("Enter due date (DD.MM.YYYY, optional): ").strip()
    due_date = due_date if due_date else None
    try:
        note = Note(title=title, content=content, tags=[tag.strip() for tag in tags], due_date=due_date)
        return notebook.add(note)
    except ValueError as e:
        return str(e)

@handle_error
def add_note_json(args, notebook: Notebook):
    """
    Add a note to the notebook from a JSON object.

    Args:
        args (list): List containing the JSON object.
        notebook (Notebook): The notebook to add the note to.

    Returns:
        str: Message indicating whether the note was added or not.
    """
    if len(args) < 1:
        return "Please provide the JSON object for the note."

    json_obj = " ".join(args)
    note = Note.from_json(json_obj)
    return notebook.add(note)

@handle_error
def show_note(args, notebook: Notebook):
    """
    Show the details of a note.

    Args:
        args (list): List containing the title of the note.
        notebook (Notebook): The notebook containing the note.

    Returns:
        str or Note: The note's details or a message indicating the note was not found.
    """
    if len(args) < 1:
        return "Please provide the title of the note."

    title = args[0]
    notes = notebook.search(title)
    if notes:
        return notebook.format_notes_with_frame(notes)
    else:
        return f"Note {title} not found."

@handle_error
def delete_note(args, notebook: Notebook):
    """
    Delete a note from the notebook.

    Args:
        args (list): List containing the title of the note.
        notebook (NoteBook): The notebook containing the note.

    Returns:
        str: Message indicating whether the note was deleted or not.
    """
    if len(args) < 1:
        return "Please provide the title of the note."

    title = args[0]
    return notebook.remove(title)

@handle_error
def delete_all_notes(args, notebook: Notebook):
    """
    Delete all notes from the notebook.

    Args:
        args (list): List of arguments.
        notebook (Notebook): The notebook containing the notes.

    Returns:
        str: Message indicating whether the notes were deleted or not.
    """
    return notebook.remove_all()

@handle_error
def update_note_prompt(args, notebook: Notebook):
    """
    Update a note in the notebook via user prompt.

    Args:
        args (list): List of arguments.
        notebook (Notebook): The notebook containing the note.

    Returns:
        str: Message indicating whether the note was updated or not.
    """
    if len(args) < 1:
        return "Please provide the title of the note to update."

    title = args[0]
    content = input("Enter new content: ")
    tags = input("Enter new tags (comma-separated): ").split(",")
    due_date = input("Enter new due date (DD.MM.YYYY, optional): ").strip()
    due_date = due_date if due_date else None
    try:
        new_note = Note(title=title, content=content, tags=[tag.strip() for tag in tags], due_date=due_date)
        return notebook.update(title, new_note)
    except ValueError as e:
        return str(e)

@handle_error
def search_notes(args, notebook: Notebook):
    """
    Search for notes containing the query in their title or content.

    Args:
        args (list): List containing the search query.
        notebook (Notebook): The notebook containing the notes.

    Returns:
        str: Search results or a message indicating no notes were found.
    """
    if len(args) < 1:
        return "Please provide the search query."

    query = args[0]
    results = notebook.search(query)
    if results:
        return notebook.format_notes_with_frame(results)
    else:
        return f"No notes found containing '{query}'."

@handle_error
def filter_notes(args, notebook: Notebook):
    """
    Filter notes by tag.

    Args:
        args (list): List containing the tag to filter by.
        notebook (Notebook): The notebook containing the notes.

    Returns:
        str: Filter results or a message indicating no notes were found.
    """
    if len(args) < 1:
        return "Please provide the tag to filter by."

    tag = args[0]
    results = notebook.filter_by_tag(tag)
    if results:
        return notebook.format_notes_with_frame(results)
    else:
        return f"No notes found with tag '{tag}'."

@handle_error
def notes_due(args, notebook: Notebook):
    """
    Get notes that are due in the next specified number of days.

    Args:
        args (list): List containing the number of days to look ahead.
        notebook (Notebook): The notebook containing the notes.

    Returns:
        str: List of due notes or a message indicating no notes are due.
    """
    if len(args) < 1:
        return "Please provide the number of days to look ahead for due notes."
    
    days = int(args[0])
    results = notebook.notes_due_in_days(days)
    if results:
        return notebook.format_notes_with_frame(results)
    else:
        return f"No notes due in the next {days} days."

@handle_error
def print_all_notes(args, notebook: Notebook):
    """
    Print all notes in the notebook.

    Args:
        args (list): List of arguments.
        notebook (Notebook): The notebook containing the notes.

    Returns:
        str: String representation of all notes.
    """
    return notebook.print_all_notes()


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

    notebook = Notebook.load_from_file("notebook.json")

    # Adding 5 dummy notes for the demo purposes.
    dummy_notes = [
        Note(
            title="Grocery Shopping",
            content="Buy fruits and vegetables",
            tags=["shopping", "errand"],
            due_date="20.05.2024"
        ),
        Note(
            title="Doctor Appointment",
            content="Annual checkup at the clinic",
            tags=["health", "appointment"],
            due_date="22.05.2024"
        ),
        Note(
            title="Project Deadline",
            content="Submit the final project report",
            tags=["work", "important"],
            due_date="25.05.2024"
        ),
        Note(
            title="Birthday Party",
            content="Celebrate John's birthday at his house",
            tags=["party", "celebration"],
            due_date="21.05.2024"
        ),
        Note(
            title="Yoga Class",
            content="Morning yoga session at the gym",
            tags=["exercise", "health"],
            due_date="23.05.2024"
        )
    ]
    for note in dummy_notes:
        notebook.add(note, suppress_message=True)

    """
    Main function to run the assistant bot.

    Continuously prompts the user for commands and executes the appropriate function.
    """
    book = load_data()
    print(handler.greeting())
    while True:
        style = Style.from_dict(INPUT_STYLE)
        completer = ContactCompleter(Menu.get_commands_witn_args(), book)
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
                print(*get_upcoming_birthdays(args, book), sep="\n")
            case "update_contact_email":
                print(update_contact_email(args, book))
            case "add-note":
                print(add_note_prompt(args, notebook))
            case "find-note":
                print(show_note(args, notebook))
            case "update-note":
                print(update_note_prompt(args, notebook))
            case "delete-note":
                print(delete_note(args, notebook))
            case "delete-all-notes":
                print(delete_all_notes(args, notebook))
            case "search-notes":
                print(search_notes(args, notebook))
            case "filter-notes":
                print(filter_notes(args, notebook))
            case "notes-due":
                print(notes_due(args, notebook))
            case "all-notes":
                print(print_all_notes(args, notebook))
            case "help":
                print("Allowed commands:")
                print(*Menu.get_commands_list(), sep="\n")
            case _:
                command = user_input.split()[0]
                suggestions = Menu.suggest_similar_commands(command)
                if suggestions:
                    print(
                        f"Command '{command}' not found. Did you mean: {', '.join(suggestions)}?"
                    )
                else:
                    print(f"Command '{command}' not found.")


if __name__ == "__main__":
    main()
