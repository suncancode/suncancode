# instance_class_attributes.py
# Demonstrates instance and class attributes

class Student:
    # Class attributes (common to all)
    email_domain = "solla.sollew.edu"
    student_dir = "/user/student"

    def __init__(self, id, first_name, last_name):
        # Instance attributes (unique to each object)
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

# Creating objects
student1 = Student("0973427", "John", "Smith")
student2 = Student("1882845", "Mary", "Wilson")

# Accessing instance attributes
print(student1.id)  # 0973427
print(student2.first_name)  # Mary

# Accessing class attributes
print(Student.email_domain)  # solla.sollew.edu
print(Student.student_dir)  # /user/student