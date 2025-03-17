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


# Тестування:
st1 = Student('M', 41, 'FFF', 'rrrr', 'A17')
st2 = Student('M', 41, 'FFF', 'rrrrr', 'A17')
st3 = Student('M', 41, 'FFF', 'eeeee', 'A17')
st4 = Student('M', 41, 'FFF', 'yyyy', 'A17')
st5 = Student('M', 41, 'FFF', 'jjjjj', 'A17')
st6 = Student('M', 41, 'FFF', 'tttt', 'A17')
st7 = Student('M', 41, 'FFF', 'qqqq', 'A17')
st8 = Student('M', 41, 'FFF', 'uuuu', 'A17')
st9 = Student('M', 41, 'FFF', 'yu', 'A17')
st10 = Student('M', 41, 'FFF', 'rt', 'A17')
st11 = Student('M', 41, 'FFF', 'ssss', 'A17')

gr = Group('R145')
gr.add_student(st1)
gr.add_student(st2)
gr.add_student(st3)
gr.add_student(st4)
gr.add_student(st5)
gr.add_student(st6)
gr.add_student(st7)
gr.add_student(st8)
gr.add_student(st9)
gr.add_student(st10)

print(len(gr.group))

gr.add_student(st11)

