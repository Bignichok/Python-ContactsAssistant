from AddressBook import AddressBook
from Record import Record
from dataHelpers import save_data, load_data
from Notebook import NoteBook
from Note import Note

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
def remove_contact(args, book: AddressBook):
    """
    Removes an contact from address book.

    Args:
        args (list): List containing contact name.
        book (AddressBook): The address book.

    Returns:
        str: Message indicating whether the contact was added or updated.
    """
    name = args[0]
    if book.delete(name) is None:
        return f"Contact with name {name} does not exist."
    return "Contact removed."


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
            return "Birthday not added to this contact."
    else:
        return not_found_message


@handle_error
def add_note_prompt(args, notebook: NoteBook):
    """
    Add a note to the notebook via user prompt.

    Args:
        args (list): List of arguments.
        notebook (NoteBook): The notebook to add the note to.

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
def add_note_json(args, notebook: NoteBook):
    """
    Add a note to the notebook from a JSON object.

    Args:
        args (list): List containing the JSON object.
        notebook (NoteBook): The notebook to add the note to.

    Returns:
        str: Message indicating whether the note was added or not.
    """
    if len(args) < 1:
        return "Please provide the JSON object for the note."
    
    json_obj = " ".join(args)
    note = Note.from_json(json_obj)
    return notebook.add(note)

@handle_error
def show_note(args, notebook: NoteBook):
    """
    Show the details of a note.

    Args:
        args (list): List containing the title of the note.
        notebook (NoteBook): The notebook containing the note.

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
def delete_note(args, notebook: NoteBook):
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
def delete_all_notes(args, notebook: NoteBook):
    """
    Delete all notes from the notebook.

    Args:
        args (list): List of arguments.
        notebook (NoteBook): The notebook containing the notes.

    Returns:
        str: Message indicating whether the notes were deleted or not.
    """
    return notebook.remove_all()

@handle_error
def update_note_prompt(args, notebook: NoteBook):
    """
    Update a note in the notebook via user prompt.

    Args:
        args (list): List of arguments.
        notebook (NoteBook): The notebook containing the note.

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
def search_notes(args, notebook: NoteBook):
    """
    Search for notes containing the query in their title or content.

    Args:
        args (list): List containing the search query.
        notebook (NoteBook): The notebook containing the notes.

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
def filter_notes(args, notebook: NoteBook):
    """
    Filter notes by tag.

    Args:
        args (list): List containing the tag to filter by.
        notebook (NoteBook): The notebook containing the notes.

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
def notes_due(args, notebook: NoteBook):
    """
    Get notes that are due in the next specified number of days.

    Args:
        args (list): List containing the number of days to look ahead.
        notebook (NoteBook): The notebook containing the notes.

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
def print_all_notes(args, notebook: NoteBook):
    """
    Print all notes in the notebook.

    Args:
        args (list): List of arguments.
        notebook (NoteBook): The notebook containing the notes.

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


def get_allowed_commands():
    return [
        "close",
        "exit",
        "add",
        "change",
        "remove",
        "all",
        "phone",
        "addphone",
        "removephone",
        "updatephone",
        "add-birthday",
        "show-birthday",
        "change-email",
        "birthdays",
        "add-note",
        "find-in-note-title",
        "update-note",
        "delete-note",
        "delete-all-notes",
        "search-notes",
        "filter-notes-by-tag",
        "notes-due",
        "all-notes"
    ]


def main():
    notebook = NoteBook.load_from_file("notebook.json")
    # Demo-notes. Must be deleted before production
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
            case "remove":
                print(remove_contact(args, book))
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
            case "add-note":
                print(add_note_prompt(args, notebook))
            case "find-in-note-title":
                print(show_note(args, notebook))
            case "update-note":
                print(update_note_prompt(args, notebook))
            case "delete-note":
                print(delete_note(args, notebook))
            case "delete-all-notes":
                print(delete_all_notes(args, notebook))
            case "search-notes":
                print(search_notes(args, notebook))
            case "filter-notes-by-tag":
                print(filter_notes(args, notebook))
            case "notes-due":
                print(notes_due(args, notebook))
            case "all-notes":
                print(print_all_notes(args, notebook))
            case "help":
                print("Allowed commands:")
                print(get_allowed_commands())
            case _:
                print("Invalid command.")


if __name__ == "__main__":
    main()