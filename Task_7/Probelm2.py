class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, name):
        self.students.append(name)

    def count_students(self):
        return len(self.students)


# Test
c = Classroom()
c.add_student("Ali")
c.add_student("Sara")
print(c.count_students())