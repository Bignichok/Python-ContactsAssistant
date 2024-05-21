from Phone import Phone
from Name import Name
from Birthday import Birthday
from Email import Email

class Record:
    """
    A class to represent a contact record.

    Attributes:
        name (Name): The name of the contact.
        phones (list): A list of phone numbers associated with the contact.
        birthday (Birthday): The birthday of the contact.

    Methods:
        __init__(name): Initializes the Record with a given name.
        __str__(): Returns a string representation of the contact record.
        add_phone(number): Adds a phone number to the contact record.
        remove_phone(number): Removes a phone number from the contact record.
        edit_phone(old_number, new_number): Edits a phone number in the contact record.
        find_phone(number): Finds a phone number in the contact record.
        add_birthday(date): Adds a birthday to the contact record.
    """
    def __init__(self, name):
        """
        Initializes the Record instance with the given name.

        Args:
            name (str): The name of the contact.
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = ''

    def __str__(self):
        """
        Returns a string representation of the contact record.

        Returns:
            str: A string containing the name, phone numbers, and birthday of the contact.
        """
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, email: {self.email}"
        if self.birthday:
            result += f", birthday: {self.birthday}"
        return result

    def add_phone(self, number: str):
        """
        Adds a phone number to the contact record.

        Args:
            number (str): The phone number to be added.
        """
        self.phones.append(Phone(number))
        
    def remove_phone(self, number: str):
        """
        Removes a phone number from the contact record.

        Args:
            number (str): The phone number to be removed.
        """
        self.phones = list(filter(lambda phone: phone == number,self.phones))
        
    def edit_phone(self, old_number: str, new_number: str):
        """
        Edits a phone number in the contact record.

        Args:
            old_number (str): The current phone number to be replaced.
            new_number (str): The new phone number to replace the old one with.

        Raises:
            KeyError: If the provided number does not exist or the contact has no phone numbers.
        """
        found = False
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                found = True
                break
        if not found:
            raise KeyError('Provided number does not exist or contact has no phone numbers.')
        
    def find_phone(self, number):
        """
        Finds a phone number in the contact record.

        Args:
            number (str): The phone number to find.

        Returns:
            Phone: The phone number object if found, otherwise None.
        """
        for phone in self.phones:
            if phone.value == number:
                return phone
            
    def add_birthday(self, date):
        """
        Adds a birthday to the contact record.

        Args:
            date (str): The birthday date string in the format specified by DATE_FORMAT: "%d.%m.%Y".
        """
        self.birthday = Birthday(date)

    def add_email(self, email: str):
        """
        Adds and validates the user's email address.
        
        Args:
            email (str): The email address to be validated and added.
        
        Raises:
            ValueError: If the email address format is invalid.
        """
        self.email = Email(email)
