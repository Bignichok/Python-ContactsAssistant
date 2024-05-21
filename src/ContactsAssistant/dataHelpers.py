import pickle

from AddressBook import AddressBook

FILENAME = "./src/ContactsAssistant/addressbook.pkl"

def save_data(book, filename=FILENAME):
    """
    Saves the address book data to a file using pickle.

    Args:
        book (AddressBook): The address book object to be saved.
        filename (str): The name of the file where the data will be saved. Defaults to FILENAME.

    Raises:
        Exception: If there is an error during the file operation.
    """
    try:
        with open(filename, "wb") as file:
            pickle.dump(book, file)
    except Exception as e:
        raise Exception(f"Error saving data: {e}")

def load_data(filename=FILENAME):
    """
    Loads the address book data from a file using pickle.

    Args:
        filename (str): The name of the file from which the data will be loaded. Defaults to FILENAME.

    Returns:
        AddressBook: The loaded address book object. If the file does not exist, returns a new AddressBook instance.

    Raises:
        Exception: If there is an error during the file operation other than FileNotFoundError.
    """
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()
    except Exception as e:
        raise Exception(f"Error loading data: {e}")