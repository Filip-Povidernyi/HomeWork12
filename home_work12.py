from collections import UserDict
from datetime import datetime, date
import pickle
import re


class Field:

    def __init__(self, value) -> None:
        self.value = value

class Name(Field):

    def __init__(self, value):
        super().__init__(value)



class Phone(Field):

    def __init__(self, value):
        super().__init__(value)
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):

        if not isinstance(new_value, str):
            raise ValueError("Phone must be a string")

        if not all(c.isdigit() for c in new_value):
            raise ValueError("Phone must contain only digits")

        if not new_value:
            raise ValueError("Phone must not be empty")

        self._value = new_value

    

class Email(Field):

    def __init__(self, value):
        super().__init__(value)
        self.value = value
        
    @property
    def email(self):
        return self._value
    
    @email.setter
    def email(self, new_value):

        if not isinstance(new_value, str):
            raise ValueError('Email must be a string')
        
        if not re.match(r"^[a-z]+[a-zA-Z0-9._-]+\@\w+\w{2:}", new_value):
            raise ValueError("E-mail value must be a valid e-mail address")

        self._value = new_value



class Birthday(Field):

    def init(self, value):
        self.value = self.validate(value)

    def validate(self, value):

        if not isinstance(value, str):
            raise ValueError("Birthday must be a string")

        try:
            birthday = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Birthday must be in format 'YYYY-MM-DD'")

        if birthday > date.today():
            raise ValueError("Birthday must not be in the future")

        return birthday

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):

        self._value = self.validate(new_value)



class Record:
    
    def __init__(self, name: str, phone: Phone=None, email: Email=None, birthday: Birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []
        self.emails = []
        if phone:
            self.phones.append(phone)
        if email:
            self.emails.append(email)
        if birthday:
            self.birthday = birthday

    def add_phone(self, phone):

        if not isinstance(phone, Phone):
            raise ValueError("Phone must be an instance of Phone class")
        else:
            self.phones.append(phone)

    def remove_phone(self, phone):

        if not isinstance(phone, Phone):
            raise ValueError("Phone must be an instance of Phone class")
        else:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):

        if not isinstance(old_phone, Phone) or not isinstance(new_phone, Phone):
            raise ValueError("Phone must be an instance of Phone class")
        else:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone

    def add_email(self, email):

        if not isinstance(email, Email):
            raise ValueError("E-mail must be an instance of Email class")
        else:
            self.emails.append(email)

    def remove_email(self, email):

        if not isinstance(email, Email):
            raise ValueError("E-mail must be an instance of Email class")
        else:
            self.emails.remove(email)

    def edit_email(self, old_email, new_email):

        if not isinstance(old_email, Email) or not isinstance(new_email, Email):
            raise ValueError('E-mail must be an instance of Email class')
        else:
            index = self.emails.index(old_email)
            self.emails[index] = new_email

    def days_to_birthday(self):

        if not self.birthday:
            return None

        today = date.today()
        next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)

        if next_birthday < today:
            next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)

        delta = next_birthday - today

        return delta.days
    
class AddressBook(UserDict):

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def add_record(self, record):
        self.data[rec.name.value] = record
        print(self.data)

    def iterator(self, n):

        if not isinstance(n, int) or n <= 0:
            raise ValueError("n must be a positive integer")

        keys = list(self.data.keys())
        pages = len(keys) // n + 1

        for i in range(pages):

            start = i * n
            end = (i + 1) * n

        page = ""
        for key in keys[start:end]:

            record = self.data[key]
            page += str(record) + "\n"
            
            yield page

    def save_to_file(self, filename):

        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):

        with open(filename, 'rb') as file:
            self.data = pickle.load(file)

    def search(self, query):

        results = []
        for record in self.data.values():

            query = query.lower()
            name = record.name.value.lower()
            phones = [phone.value for phone in record.phones]
            emails = [email.value.lower() for email in record.emails]

        if query in name or any(query in phone for phone in phones) or any(query in email for email in emails):
            results.append(record)
            
        return results
        

if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('1234567890')
    email = Email('example@gmail.com')
    birthday = Birthday('1986-04-27')
    rec = Record(name, phone, email, birthday)
    print(rec.days_to_birthday())
    ab = AddressBook()
    ab.add_record(rec)
    
