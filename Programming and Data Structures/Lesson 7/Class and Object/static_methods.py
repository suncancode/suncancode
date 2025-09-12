# static_methods.py
# Demonstrates static methods

class Student:
    @staticmethod
    def uni_website():
        """Returns the University website address"""
        return "http://www.solla.sollew.edu"

# Calling static method
print("Uni website: " + Student.uni_website())  # http://www.solla.sollew.edu