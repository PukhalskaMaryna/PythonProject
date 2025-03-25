class Human:
    def __init__(self, gender, age, first_name, last_name):
        self.gender = gender
        self.age = age
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"Ім'я: {self.first_name} {self.last_name}, стать: {self.gender}, вік: {self.age} р."


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


class ErrorForMaxCount(Exception):
    """Виключення, коли група перевищує ліміт студентів"""
    def __init__(self, msg = "У групі може бути не більше 10 студентів"):
        self.msg = msg
        super().__init__(self.msg)


class Group:
    def __init__(self, number):
        self.number = number
        self.group = []

    def add_student(self, student):
        if len(self.group) >= 10:
            raise ErrorForMaxCount()
        self.group.append(student)

    def find_student(self, last_name):
        for student in self.group:
            if student.last_name == last_name:
                return student
        return None

    def delete_student(self, last_name):
        student_delete = self.find_student(last_name)
        if student_delete:
            self.group.remove(student_delete)

    def __str__(self):
        all_students = '\n'.join(str(student) for student in self.group)
        return f'Група: {self.number}\n{all_students}'

# st1 = Student("чоловіча", 30, "Стив", "Jobs", "11111")
# st2 = Student("чоловіча", 22, "Біл", "Гейтс", "22222")
#
# gr = Group(101)
# gr.add_student(st1)
# gr.add_student(st2)
#
# assert gr.find_student('Jobs') == st1  # Перевірка, чи знайшовся студент "Jobs" і чи дорівнює він st1
#
# print("ок")

