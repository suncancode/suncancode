# generate_password.py
# Demonstrates function to generate password from username

def transform_character(letter):
    letter = letter.lower()
    if letter == "i":
        return "1"
    elif letter == "r":
        return "7"
    elif letter == "s":
        return "5"
    elif letter == "z":
        return "2"
    else:
        return letter

def generate_password(username):
    password = ""
    for i in range(0, len(username)):
        letter = username[i]
        password_letter = transform_character(letter)
        password += password_letter
    return password

# Test
username = input("Enter username: ")
password = generate_password(username)
print("Password is " + password)