from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if len(value) != 10:
            raise ValueError("The phone number should contain 10 numbers")
        else:
              self.value = value


class Birthday(Field):
    def __init__(self, value):
        try:
             self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))


    def remove_phone(self, phone):
        "This method checks if the phone number exists in the list and deletes it"
        for p in self.phones:
              if p.value == phone:
                  self.phones.remove(p)
                  return
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone, new_phone):
          "This method checks that the old phone number is exist in the list and edit it "
          for p in self.phones:
                if p.value == old_phone: 
                    p.value = Phone(new_phone).value
                    return
          raise ValueError("Phone number not found")
    
    def find_phone(self, phone):
          "This method checks if the phone number exists in the list and returns it"
          for p in self.phones:
                if p.value == phone:
                      return p
          raise ValueError("Phone number not found")
    

    def add_birthday(self, birthday):
         self.birthday = Birthday(birthday)
         
          
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
     def add_record(self, record):
          self.data[record.name.value] = record

     def find(self, name):
          return self.data.get(name, None)
     
     def delete(self, name):
          if name in self.data:
               del self.data[name]

     def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        current_day = datetime.today().date()
        
        for record in self.data.values():
            if record.birthday:
                # Get the birthday date for the current year
                birthday_this_year = record.birthday.value.replace(year=current_day.year)
                
                # If the birthday has already passed this year, move it to the next year
                if birthday_this_year < current_day:
                    birthday_this_year = birthday_this_year.replace(year=current_day.year + 1)
                
                # Calculate the number of days until the birthday
                days_until_birthday = (birthday_this_year - current_day).days
                
                # Check if the birthday falls within the next week
                if 0 <= days_until_birthday <= 7:
                    congratulation_date = birthday_this_year
                    
                    # If the birthday falls on a weekend, move the celebration to Monday
                    if congratulation_date.weekday() in (5, 6):
                        congratulation_date += timedelta(days=(7 - congratulation_date.weekday()))
                    
                    # Add the contact to the upcoming birthday list
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        
        return upcoming_birthdays
     
def input_error(func):
    """Decorator to handle input errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Error: Provide both a name and a phone number."
    name, phone, *_ = args
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_phone(args, book):
    """Changes the phone number for an existing contact."""
    if len(args) < 3:
        return "Error: Provide both a name, a phone number and new phone number"
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} not found.")
    record.edit_phone(old_phone, new_phone)
    return f"Phone number for {name} changed to {new_phone}."

@input_error
def show_phone(args, book):
    """Displays all phone numbers for a given contact."""
    if len(args) < 1:
        return "Error: Provide a name"
    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} not found.")
    return f"{name}: {', '.join(p.value for p in record.phones)}"

@input_error
def show_all(book):
    """Displays all contacts with their phone numbers."""
    if not book.data:
        return "The address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    # Args will contain the contact name and the birthday in DD.MM.YYYY format
    if len(args) < 2:
        return "Error: Provide a name and birthday"
    name, birthday = args
    record = book.find(name)
    if not record:
        raise ValueError(f"Contact with the name {name} not found.")
    record.add_birthday(birthday)
    return f"Birthday {birthday} added to {name}."

@input_error
def show_birthday(args, book: AddressBook):
    # Args will contain the contact name
    if len(args) < 1:
        return "Error: Provide a name"
    name = args[0]
    record = book.find(name)
    if not record or not record.birthday:
        raise ValueError(f"Birthday for contact {name} not found.")
    return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."

@input_error
def birthdays(args, book: AddressBook):
    # Args are not used, as the book will provide the necessary info
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays this week."
    
    result = []
    for contact in upcoming_birthdays:
        result.append(f"{contact['name']} - {contact['congratulation_date']}")
    
    return "\n".join(result)
    

