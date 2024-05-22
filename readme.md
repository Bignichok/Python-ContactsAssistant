# Contacts Assistant

Contacts Assistant is a bot designed to help you manage your address book efficiently. Below is a list of available commands, their functions, and required arguments.

## List of Commands

- **"hello"**: 
  - *Greeting*
  - **Arguments**: None

- **"close" | "exit"**: 
  - *Save the current state and stop the bot assistant*
  - **Arguments**: None

- **"add"**: 
  - *Add a contact to the address book or update an existing contact*
  - **Arguments**: `name`, `phone_number`, `email`, `address`

- **"change"**: 
  - *Change the phone number of an existing contact*
  - **Arguments**: `name`, `old_number`, `new_number`

- **"phone"**: 
  - *Show the phone number of a contact*
  - **Arguments**: `name`

- **"all"**: 
  - *Returns a string representation of the address book*
  - **Arguments**: None

- **"add-birthday"**: 
  - *Add a birthday to a contact*
  - **Arguments**: `name`, `date %d.%m.%Y`

- **"show-birthday"**: 
  - *Show the birthday of a contact*
  - **Arguments**: `name`

- **"birthdays"**: 
  - *Returns a list of upcoming birthdays within the next 7 days*
  - **Arguments**: None

These commands help you manage and retrieve contact information efficiently. Use them to keep your address book organized and up-to-date.
