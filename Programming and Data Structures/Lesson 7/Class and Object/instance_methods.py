# instance_methods.py
# Demonstrates instance methods in class

class Student:
    email_domain = "solla.sollew.edu"
    student_dir = "/user/student"

    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = first_name[0].lower() + last_name[0].lower() + id[0:3]

    def fullname(self):
        return self.first_name + " " + self.last_name

    def email(self):
        return self.username + "@" + Student.email_domain

    def email_alias(self):
        return self.first_name + "." + self.last_name + "." + self.id[0:3] + "@" + Student.email_domain

    def home_dir(self):
        return Student.student_dir + "/" + self.username

    def print_detail(self):
        print("Student ID: " + self.id)
        print("First name: " + self.first_name)
        print("Last name: " + self.last_name)
        print("Full name: " + self.fullname())
        print("Username: " + self.username)
        print("Email: " + self.email())
        print("Email alias: " + self.email_alias())
        print("Home directory: " + self.home_dir())

# Test
student1 = Student("0973427", "John", "Smith")
print(student1.fullname())  # John Smith
student1.print_detail()