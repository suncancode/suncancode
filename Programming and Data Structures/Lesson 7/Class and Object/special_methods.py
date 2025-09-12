# special_methods.py
# Demonstrates special dunder methods

class Student:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return self.first_name + " " + self.last_name + " (" + self.id + ")"

    def __repr__(self):
        return "Student('" + self.id + "', '" + self.first_name + "', '" + self.last_name + "')"

# Test
student2 = Student("1882845", "Mary", "Wilson")
print(str(student2))  # Mary Wilson (1882845)
print(repr(student2))  # Student('1882845', 'Mary', 'Wilson')