import datetime

# Get user input
fname = input("Enter your first name: ")
lname = input("Enter your last name: ")
dob = input("Enter your dob (DD-MM-YYYY): ")
dob_format = input("Choose a format:  (A)bbreviated  (N)ormal: ")

# Displaying table of user information based on dob format
if dob_format.upper() == "A":
    dob = datetime.datetime.strptime(dob, "%d-%m-%Y").date()
    print(f"{"First name":<15}{"Last Name":<15}{"Date of Birth":<15}")
    print(f"{fname:<15}{lname:<15}{dob.strftime("%d/%b/%Y"):<15}")
elif dob_format.upper() == "N":
    dob = datetime.datetime.strptime(dob, "%d-%m-%Y").date()
    print(f"{"First name":<15}{"Last Name":<15}{"Date of Birth":<15}")
    print(f"{fname:^15}{lname:^15}{dob.strftime("%d-%m-%Y"):^15}")
else:
    dob = datetime.datetime.strptime(dob, "%d-%m-%Y").date()
    print(f"{"First name":<15}{"Last Name":<15}{"Date of Birth":<15}")
    print(f"{fname:^15}{lname:^15}{dob.strftime("%d-%m-%Y"):<15}")