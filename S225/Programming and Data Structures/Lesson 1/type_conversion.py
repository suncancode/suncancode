# type_conversion.py
# demonstrate type conversion in Python

# converting to string
fav_number = 369
fav_number_str =  str(fav_number)
print("My favorite number as string:", fav_number_str) 
# output: 

# converting string input to integer
try:
    user_input = input("Enter an integer: ")
    number = int(user_input)
    print("Converted integer:", number)
except ValueError:
    print("Invalid input!")

# converting int input to float
try:
    user_input = input("Enter an integer: ")
    number = float(user_input)
    print("Converted float: ", number)
except ValueError:
    print("Invalid input!")

# converting to boolean
non_empty_string = "hehe"
empty_string = ""
print("Non-empty string to boolean:", bool(non_empty_string)) # output: True
print("Empty string to boolean:", bool(empty_string)) # output: False