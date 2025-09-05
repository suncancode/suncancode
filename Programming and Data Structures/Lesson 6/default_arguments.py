# default_arguments.py
# Demonstrates default arguments in function

def welcome(name, greeting="Hi"):
    print("{0} {1}!".format(greeting, name))

# Test
welcome("John", "Hello")  # Hello John!
welcome("Mary", greeting="It is nice to meet you")  # It is nice to meet you Mary!
welcome("Paul")  # Hi Paul!