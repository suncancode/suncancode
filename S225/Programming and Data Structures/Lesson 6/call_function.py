# call_function.py
# Demonstrates calling functions with different arg and return counts

def add_two_numbers(number1, number2):
    return number1 + number2

# Calling with 2 args, 1 return
number1 = add_two_numbers(4, 3)
print(number1)  # 7

number2 = add_two_numbers(2, number1)
print(number2)  # 9

number3 = add_two_numbers(number2, number2)
print(number3)  # 18

number4 = add_two_numbers(number3, 10)
print(number4)  # 28