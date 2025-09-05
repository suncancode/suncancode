# define_function.py
# Demonstrates basic function definition and declaration

# Function with args and return
def add_two_numbers(number1, number2):
    return number1 + number2

# Function with no args and return
def ask_name():
    first_name = "Finley"
    last_name = "Fish"
    return first_name, last_name

# Function with args and no return
def say_hello(first_name, last_name):
    print("Hello {0} {1}!".format(first_name, last_name))

# Test
print(add_two_numbers(4, 3))  # 7
first, last = ask_name()
say_hello(first, last)  # Hello Finley Fish!