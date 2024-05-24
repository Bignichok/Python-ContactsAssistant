# Contacts Assistant

Contacts Assistant is a bot designed to help you manage your address book efficiently. Below is a list of available commands, their functions, and required arguments. Additionally you can add your notes to our notebook

## Initialization
  1. Initialize virtual environment
     - .venv\Scripts\activate.bat - Windows у командному рядку (CMD)
     - .venv\Scripts\Activate.ps1 - Windows у PowerShell
     - source .venv/bin/activate - macOS та Linux
  2. pip install -r requirements.txt
  3. python src\ContactsAssistant\__main__.py
  4. use one of commands presented below (bot will suggest you commands and named arguments that you need)

## List of Commands

### Contacts Book
- **"hello"**: 
  - *Greeting*
  - **Arguments**: None

- **"close" | "exit"**: 
  - *Save the current state and stop the bot assistant*
  - **Arguments**: None

- **"add_contact"**: 
  - *Add a contact to the address book or update an existing contact*
  - **Arguments**: `name`, `phone`, `email`, `birthday`

- **"update_contact"**: 
  - *Change the phone number of an existing contact*
  - **Arguments**: `name`, `oldphone`, `newphone`

- **"delete_contact"**: 
  - *Delete contact by name*
  - **Arguments**: `name`

- **"set_contact_birthday"**: 
  - *Add a birthday to a contact*
  - **Arguments**: `name`, `date %d.%m.%Y`

- **"get_contact_birthday"**: 
  - *Show the birthday of a contact*
  - **Arguments**: `name`

- **"get_contact_by_name"**: 
  - *Find contact by name*
  - **Arguments**: `name`

- **"get_contact_by_phone"**: 
  - *Find contact by phone*
  - **Arguments**: `phone`

- **"get_contact_by_email"**: 
  - *Find contact by email*
  - **Arguments**: `email`

- **"get_all_contacts"**: 
  - *Returns a string representation of the address book*
  - **Arguments**: None

- **"get_upcoming_birthdays"**: 
  - *Returns a list of upcoming birthdays within the next 7 days*
  - **Arguments**: None

- **"update_contact_email"**: 
  - *Update contact email*
  - **Arguments**: `name`, `email`

- **"add_address"**: 
  - *Update contact address*
  - **Arguments**: `name`, `addresstype`, `street`, `city`, `postalcode`, `country`

- **"delete_address"**: 
  - *Delete contact address*
  - **Arguments**: `name`, `addresstype`

### NoteBook
- **"add_note"**: 
  - *Add note*
  - **Arguments**: None

- **"find_note"**: 
  - *Find note by title*
  - **Arguments**: `title`

- **"delete_note"**: 
  - *Delete note by title*
  - **Arguments**: `title`

- **"delete_all_notes"**: 
  - *Delete note by title*
  - **Arguments**: None

- **"update_note"**: 
  - *Update note by title*
  - **Arguments**: `title`

- **"search_notes"**: 
  - *Search for notes containing the query in their title or content.*
  - **Arguments**: `query`

- **"filter_notes_by_tag"**: 
  - *Filter notes by tag.*
  - **Arguments**: `tag`

- **"get_notes_in_days"**: 
  - *Get notes that are due in the next specified number of days.*
  - **Arguments**: `days`

- **"get_all_notes"**: 
  - *to view a full notes list*
  - **Arguments**: None

These commands help you manage and retrieve contact information and notes efficiently. Use them to keep your contacts book organized and up-to-date.
