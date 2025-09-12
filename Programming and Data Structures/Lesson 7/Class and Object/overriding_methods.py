# overriding_methods.py
# Demonstrates overriding methods in inheritance

class Student:
    student_dir = "/user/student"

    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = first_name[0].lower() + last_name[0].lower() + id[0:3]

    def fullname(self):
        return self.first_name + " " + self.last_name

    def home_dir(self):
        return Student.student_dir + "/" + self.username

    def print_detail(self):
        print("Student ID: " + self.id)
        print("First name: " + self.first_name)
        print("Last name: " + self.last_name)
        print("Full name: " + self.fullname())
        print("Username: " + self.username)
        print("Home directory: " + self.home_dir())

class PostGradStudent(Student):
    student_dir = "/user/poststudent"

    def __init__(self, id, first_name, last_name, thesis):
        super().__init__(id, first_name, last_name)
        self.thesis = thesis

    def home_dir(self):
        """Override the parent method with a new directory"""
        return PostGradStudent.student_dir + "/" + self.username

    def print_detail(self):
        """Display student detail"""
        super().print_detail()
        print("Thesis: " + self.thesis)

# Test
pg_student1 = PostGradStudent("0945720", "Adrian", "Creedon", "Polynomial Approximation of Functions")
pg_student1.print_detail()