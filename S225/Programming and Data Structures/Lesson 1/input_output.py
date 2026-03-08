# input_output.py
# demonstrate input and output functions in Python

# basic print function
print("Hello World!") # Output: Hello World!
print("Welcome to Python! ", end="<3")  # Output: Welcome to Python! <3

# getting user input
first_name = input("Enter your First name: ")
last_name = input("Enter your Last name: ")
full_name = first_name + " " + last_name
print("Your name is " + full_name + ".")

# asking for multiple inputs
print("Please choose 3 dishes")
dish1 = input("Please choose your appetizer:")
dish2 = input("Please choose your main course:")
dish3 = input("Please choose your dessert:")
print("You have ordered: " + dish1 + " " + dish2 + " " + dish3 + ".")