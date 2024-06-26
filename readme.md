# Contacts Assistant

Contacts Assistant is a bot designed to help you manage your address book efficiently. Below is a list of available commands, their functions, and required arguments. Additionally you can add your notes to our notebook

## Initialization
  ### locally
  1. Initialize virtual environment
     - .venv\Scripts\activate.bat - Windows CMD
     - .venv\Scripts\Activate.ps1 - Windows PowerShell
     - source .venv/bin/activate - macOS, Linux
  2. pip install -r requirements.txt
  3. python src\main.py
  4. use one of commands presented below (bot will suggest you commands and named arguments that you need)
  ### installed package
  1. Initialize virtual environment
     - .venv\Scripts\activate.bat - Windows CMD
     - .venv\Scripts\Activate.ps1 - Windows PowerShell
     - source .venv/bin/activate - macOS, Linux
  2. pip install contacts-assistant
  3. contacts_assistant

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

- **"update_phone"**: 
  - *Change the phone number of an existing contact*
  - **Arguments**: `name`, `oldphone`, `newphone`

- **"delete_contact"**: 
  - *Delete contact by name*
  - **Arguments**: `name`

- **"set_birthday"**: 
  - *Add a birthday to a contact*
  - **Arguments**: `name`, `date %d.%m.%Y`

- **"show_birthday"**: 
  - *Show the birthday of a contact*
  - **Arguments**: `name`

- **"find_contact_by_name"**: 
  - *Find contact by name*
  - **Arguments**: `name`

- **"find_contact_by_phone"**: 
  - *Find contact by phone*
  - **Arguments**: `phone`

- **"find_contact_by_email"**: 
  - *Find contact by email*
  - **Arguments**: `email`

- **"show_all_contacts"**: 
  - *Returns a string representation of the address book*
  - **Arguments**: None

- **"upcoming_birthdays"**: 
  - *Returns a list of upcoming birthdays within the specified number of days*
  - **Arguments**: `days`

- **"update_email"**: 
  - *Update contact email*
  - **Arguments**: `name`, `email`

- **"add_address"**: 
  - *Add or update the address of a contact*
  - **Arguments**: `name`, `addresstype`, `street`, `city`, `postalcode`, `country`

- **"remove_address"**: 
  - *Remove the address of a contact*
  - **Arguments**: `name`, `addresstype`

### NoteBook
- **"add_note"**: 
  - *Add a new note*
  - **Arguments**: None

- **"find_note"**: 
  - *Find a note by title*
  - **Arguments**: `title`

- **"delete_note"**: 
  - *Delete a note by title*
  - **Arguments**: `title`

- **"delete_all_notes"**: 
  - *Delete all notes*
  - **Arguments**: None

- **"update_note"**: 
  - *Update a note by title*
  - **Arguments**: `title`

- **"search_notes"**: 
  - *Search for notes containing the query in their title or content*
  - **Arguments**: `query`

- **"filter_notes_by_tag"**: 
  - *Filter notes by tag*
  - **Arguments**: `tag`

- **"notes_due_in_days"**: 
  - *Show notes that are due within the next specified number of days*
  - **Arguments**: `days`

- **"show_all_notes"**: 
  - *Show all notes*
  - **Arguments**: None

These commands help you manage and retrieve contact information and notes efficiently. Use them to keep your contacts book organized and up-to-date.
