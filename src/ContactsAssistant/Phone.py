from Field import Field

class Phone(Field):
    def __init__(self, number):
        self.value = self.validate_number(number)

    def validate_number(self, number):
        if len(number) != 10:
            raise ValueError("Telephone number should have 10 numbers")
        
        if not number.isdigit():
            raise ValueError("Telephone number should have only numbers")
        
        return number
