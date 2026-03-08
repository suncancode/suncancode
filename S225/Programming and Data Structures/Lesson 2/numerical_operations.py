# numerical_operations.py
# Demonstrates numerical operations: division, floor division, exponentiation, and compound assignments

# Basic arithmetic operators: Addition (+), Subtraction (-), Multiplication (*)

# Division vs Floor division
number1 = 10
number2 = 3
print("Regular division:", number1 / number2)  # Output: 3.3333333333333335
print("Floor division:", number1 // number2)  # Output: 3

# Exponentiation for square root
number = 16
square_root = number ** 0.5
print("Square root of", number, "is", square_root)  # Output: Square root of 16 is 4.0

# Modulus to find the last digit of positive integers
num1 = 15 
print("")

# Compound assignment operators

"""
+=      x += 2 is the same as x = x + 2 
-=      x -= 2 is the same as x = x - 2
*=      x *= 2 is the same as x = x * 2
/=      x /= 2 is the same as x = x / 2
//=     x //= 2 is the same as x = x // 2
**=     x **= 2 is the same as x = x ** 2
%=      x %= 2 is the same as x = x % 2
"""

x = 10
print("Initial x:", x)  # Output: 10
x += 2  # Equivalent to x = x + 2
print("After x += 2:", x)  # Output: 12
x //= 3  # Equivalent to x = x // 3
print("After x //= 3:", x)  # Output: 4
x **= 2  # Equivalent to x = x ** 2
print("After x **= 2:", x)  # Output: 16