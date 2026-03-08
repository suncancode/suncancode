# while_break.py
# Demonstrates while True with break to stop on 'q'

while True:
    user_input = input("Enter something (or q to quit): ")
    if user_input == "q":
        print("Goodbye!")
        break
    print("You have entered: " + user_input)
    print()  # New line