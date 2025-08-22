# break_statement.py
# Demonstrate break keywork to terminate loop early

# Flag to indicate user has answered YES
user_say_yes = False

# Ask user up to 10 times
for i in range(0, 10):
    answer = input("Would you like training? (Y/N): ")
    if answer.upper() == "Y":
        user_say_yes = True
        print("Nice choice!")
        break

# If user hasn't say yes
if not user_say_yes:
    print("Go to the gym 10 years!")