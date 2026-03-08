# Practice with basic exception handling

try:
    # Ask user to enter an integer
    user_input = input("Enter an integer: ")
    number = int(user_input)

    # Display the integer if conversion succeeds
    print("You have entered {0}".format(number))
except ValueError:
    # Handle the exception if the input is not a valid integer
    print("Error: Please enter a valid integer.")