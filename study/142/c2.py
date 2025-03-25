from c1 import Human

class Student(Human):
    def __init__(self, gender, age, first_name, last_name, record_book):
        super().__init__(gender, age, first_name, last_name)
        self.record_book = record_book

    def __str__(self):
        return f"{super().__str__()}, record book: {self.record_book}"

    def __eq__(self, other):
        if isinstance(other, Student):
            return str(self) == str(other)
        return False

