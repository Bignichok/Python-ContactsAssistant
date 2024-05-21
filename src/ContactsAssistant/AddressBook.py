from datetime import datetime, timedelta
from collections import UserDict

from constants import DATE_FORMAT

def is_weekend_day(day:int) -> bool:
    return day > 4

class AddressBook(UserDict):
    def __str__(self):
        lines = []

        for _, record in self.data.items():
            lines.append(f'{record}')
            
        return "\n".join(lines)
    
    def add_record(self, record):
        if record.name.value in self.data:
            raise KeyError(f"Record with name '{record.name.value}' already exists.")
        self.data[record.name.value] = record
            
    def find(self, name: str):
        if name in self.data:
            return self.data[name]
        else:
            return None
        
    def delete(self, name):
        del self.data[name]
        
    def get_upcoming_birthdays(self): 
        upcoming_birthdays = []
        today_date = datetime.today().date()
        for name, record in self.data.items():
            if record.birthday:
                congratulation_date = None
                birthday_date = record.birthday.value.replace(year=today_date.year).date()
                timedelta_days = (birthday_date - today_date).days

                if timedelta_days >= 0 and timedelta_days <= 7:
                    weekday = birthday_date.weekday()
                    if is_weekend_day(weekday):
                        days_delta = 2 if weekday == 5 else 1
                        congratulation_date = birthday_date + timedelta(days=days_delta)
                    else:
                        congratulation_date = birthday_date
                if congratulation_date:
                    upcoming_birthdays.append({"name": name, "congratulation_date": congratulation_date.strftime(DATE_FORMAT)})
        return upcoming_birthdays
