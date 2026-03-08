# class_basics.py
# Demonstrates defining class and creating object

# Class blueprint
class Fish:
    def __init__(self, name, color):
        self.name = name
        self.color = color

# Creating object
shark = Fish("David", "grey")
goldfish = Fish("Sun", "orange")

# Print object attribures
print(shark.name)
print(goldfish.name)