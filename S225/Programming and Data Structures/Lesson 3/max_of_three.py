# max_of_three.py
# Demonstrates single-selection (if) with finding maximum of three numbers

# Get three integers from the user
number1 = int(input("Enter the 1st integer: "))
number2 = int(input("Enter the 2nd integer: "))
number3 = int(input("Enter the 3rd integer: "))

# Find the maximum
number_max = number1
if number2 > number_max:
    number_max = number2
if number3 > number_max:
    number_max = number3

# Display the result
print("Max of {0}, {1}, {2} is {3}".format(number1, number2, number3, number_max))