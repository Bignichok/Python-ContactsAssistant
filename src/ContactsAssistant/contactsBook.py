from datetime import datetime, timedelta
from collections import UserDict

from constants import DATE_FORMAT


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

    def find_by_name(self, name: str):
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
        
    def find_by_phone(self, phone: str):
        """
        Finds and returns a record by phone number.

        Args:
            phone (str): The phone number of the record to find.

        Returns:
            The record if found, otherwise None.
        """
        for record in self.data.values():
            if record.find_phone(phone):
                return record
        return None

    def find_by_email(self, email: str):
        """
        Finds and returns a record by email address.

        Args:
            email (str): The email address of the record to find.

        Returns:
            The record if found, otherwise None.
        """
        for record in self.data.values():
            if record.email.value == email:
                return record
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

    def get_upcoming_birthdays(self):
        """
        Returns a list of upcoming birthdays within the next 7 days.
        If a birthday falls on a weekend, the congratulation date is moved to the next Monday.
        Returns:
            list: A list of dictionaries with names and congratulation dates for upcoming birthdays.
        """
        upcoming_birthdays = []
        today_date = datetime.today().date()
        for name, record in self.data.items():
            if record.birthday:
                congratulation_date = None
                birthday_date = record.birthday.value.replace(
                    year=today_date.year
                ).date()
                timedelta_days = (birthday_date - today_date).days

                if timedelta_days >= 0 and timedelta_days <= 7:
                    weekday = birthday_date.weekday()
                    if is_weekend_day(weekday):
                        days_delta = 2 if weekday == 5 else 1
                        congratulation_date = birthday_date + timedelta(days=days_delta)
                    else:
                        congratulation_date = birthday_date
                if congratulation_date:
                    upcoming_birthdays.append(
                        {
                            "name": name,
                            "congratulation_date": congratulation_date.strftime(
                                DATE_FORMAT
                            ),
                        }
                    )
        return upcoming_birthdays
