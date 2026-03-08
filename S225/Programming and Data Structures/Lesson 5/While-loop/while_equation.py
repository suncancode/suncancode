# while_equation.py
# Demonstrates displaying equations with while based on user input

# Ask user for start and end number
user_input = input("Enter start number: ")
number_start = int(user_input)

user_input = input("Enter end number: ")
number_end = int(user_input)

# Display equations
print("Equations:")
number = number_start  # Initialization
while number <= number_end:  # Conditional
    print("{0} + {1} = {2}".format(number, number, number * 2))
    number = number + 1  # Post-loop update