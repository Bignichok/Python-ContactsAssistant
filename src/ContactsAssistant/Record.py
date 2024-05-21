from Phone import Phone
from Name import Name
from Birthday import Birthday
from Email import Email

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = ''

    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, email: {self.email}"
        if self.birthday:
            result += f", birthday: {self.birthday}"
        return result

    def add_phone(self, number: str):
        self.phones.append(Phone(number))
        
    def remove_phone(self, number: str):
        self.phones = list(filter(lambda phone: phone == number,self.phones))
        
    def edit_phone(self, old_number: str, new_number: str):
        found = False
        for i, phone in enumerate(self.phones):
            if phone.value == old_number:
                self.phones[i] = Phone(new_number)
                found = True
                break
        if not found:
            raise KeyError('Provided number does not exist or contact has no phone numbers.')
        
    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
            
    def add_birthday(self, date):
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
