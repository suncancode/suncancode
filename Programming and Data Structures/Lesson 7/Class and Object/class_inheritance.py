# class_inheritance.py
# Demonstrates class inheritance

class Student:
    student_dir = "/user/student"

    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = first_name[0].lower() + last_name[0].lower() + id[0:3]

    def home_dir(self):
        return Student.student_dir + "/" + self.username

class PostGradStudent(Student):
    student_dir = "/user/poststudent"

    def __init__(self, id, first_name, last_name, thesis):
        super().__init__(id, first_name, last_name)
        self.thesis = thesis

# Test
student1 = Student("0973427", "John", "Smith")
pg_student1 = PostGradStudent("0945720", "Adrian", "Creedon", "Polynomial Approximation of Functions")

print(student1.home_dir())  # /user/student/js097
print(pg_student1.home_dir())  # /user/poststudent/ac094
print(pg_student1.thesis)  # Polynomial Approximation of Functions