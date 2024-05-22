from datetime import date
from collections import UserDict
from datehelper import DateHelper


def is_weekend_day(day: int) -> bool:
    """
    Checks if a given day is a weekend.

    Args:
        day (int): The day of the week as an integer, where Monday is 0 and Sunday is 6.

    Returns:
        bool: True if the day is a weekend (Saturday or Sunday), False otherwise.
    """
    return day > 4


class ContactsBook(UserDict):
    """
    A class to represent an address book that stores and manages records.

    Inherits from UserDict to utilize a dictionary as the underlying data structure.

    Methods:
        __str__(): Returns a string representation of the address book.
        add_record(record): Adds a new record to the address book.
        find(name): Finds and returns a record by name.
        delete(name): Deletes a record by name.
        get_upcoming_birthdays(): Returns a list of upcoming birthdays within the next 7 days.
    """

    def __str__(self):
        """
        Returns a string representation of the address book.

        Returns:
            str: A string with each record in the address book on a new line.
        """
        lines = []

        for _, record in self.data.items():
            lines.append(f"{record}")

        return "\n".join(lines)

    def add_record(self, record):
        """
        Adds a new record to the address book.

        Args:
            record: The record to be added.

        Raises:
            KeyError: If a record with the same name already exists in the address book.
        """
        if record.name.value in self.data:
            raise KeyError(f"Record with name '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    def find(self, name: str):
        """
        Finds and returns a record by name.

        Args:
            name (str): The name of the record to find.

        Returns:
            The record if found, otherwise None.
        """
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        """
        Deletes a record by name.
        Args:
            name: The name of the record to delete.

        Returns:
            The record which was deleted, if record not found returns None.
        """
        if name in self.data:
            removedcontact = self.data[name]
            del self.data[name]
            return removedcontact
        else:
            return None

    def get_upcoming_birthdays(self, days=7):
        """
        Get a list of upcoming birthdays within the specified number of days.
        If a birthday falls on a weekend, the congratulation date is moved to the next Monday.
        Args:
            days (int): The number of days to look ahead for upcoming birthdays. Defaults to 7.

        Returns:
            list: A list of dictionaries with names and congratulation dates for upcoming birthdays.
        """
        today = date.today()
        upcoming_birthdays = []
        for contact in list(
            filter(lambda x: x.birthday is not None, self.data.values())
        ):
            next_contact_birthday = DateHelper.get_next_birthday(
                contact.birthday.value, today
            )

            diffdays = (next_contact_birthday - today).days
            if diffdays in range(0, days):
                upcoming_birthdays.append(
                    f"Contact name: {contact.name.value}, congratulation date: {DateHelper.get_formated_workday(next_contact_birthday)}"
                )

        return upcoming_birthdays
