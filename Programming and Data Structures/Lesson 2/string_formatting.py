# string_formatting.py
# Demonstrates string formatting using format() method

# Basic string formatting with positional arguments
fname = "Trung Duc"
lname = "Le"
age = 26
gpa_score = 4.0

print("Hi {0} {1}".format(fname, lname))  # Output: Hi Trung Duc Le
print("Hi {2} is {0} years old".format(age, fname, lname))  # Output: Hi Le is 26 years old
print("His GPA score is {0:.2f}".format(gpa_score))  # Output: His GPA score is 4.00

# Formatted table with text alignment
print("Alkali metals:")
print()
print("{0:<15}{1:<10}{2:^25}{3:>15}".format("Element", "Symbol", "Atomic number", "Atomic weight"))
print("{0:<15}{1:<10}{2:^25}{3:>15.3f}".format("Lithium", "Li", 3, 6.94))
print("{0:<15}{1:<10}{2:^25}{3:>15.3f}".format("Sodium", "Na", 11, 22.990))
print("{0:<15}{1:<10}{2:^25}{3:>15.3f}".format("Potassium", "K", 19, 39.098))
print("{0:<15}{1:<10}{2:^25}{3:>15.3f}".format("Rubidium", "Rb", 37, 85.468))
print("{0:<15}{1:<10}{2:^25}{3:>15.3f}".format("Caesium", "Cs", 55, 132.905))
print("{0:<15}{1:<10}{2:^25}{3:>15.3f}".format("Francium", "Fr", 87, 223))  
print()
print("12345678901234567890123456789012345678901234567890123456789012345")

"""
Output:
Alkali metals:
Element        Symbol          Atomic number        Atomic weight
Lithium        Li                    3                      6.940
Sodium         Na                   11                     22.990
Potassium      K                    19                     39.098
Rubidium       Rb                   37                     85.468
Caesium        Cs                   55                    132.905
Francium       Fr                   87                    223.000
12345678901234567890123456789012345678901234567890123456789012345
--------------- : 15 spaces
{o:<15}  left alignment, using 15 spaces

Alignment:
< : left
> : right
^ : center
"""

# Another exmaple with string format with alignment
print("{0:>2} x {1:>1} = {2:>2}".format(1, 5, 1*5))
print("{0:>2} x {1:>1} = {2:>2}".format(2, 5, 2*5))
print("{0:>2} x {1:>1} = {2:>2}".format(3, 5, 3*5))
print("{0:>2} x {1:>1} = {2:>2}".format(4, 5, 4*5))
print("{0:>2} x {1:>1} = {2:>2}".format(5, 5, 5*5))
print("{0:>2} x {1:>1} = {2:>2}".format(6, 5, 6*5))
print("{0:>2} x {1:>1} = {2:>2}".format(7, 5, 7*5))
print("{0:>2} x {1:>1} = {2:>2}".format(8, 5, 8*5))
print("{0:>2} x {1:>1} = {2:>2}".format(9, 5, 9*5))
print("{0:>2} x {1:>1} = {2:>2}".format(10, 5, 10*5))

"""
Output:
 1 x 5 =  5
 2 x 5 = 10
 3 x 5 = 15
 4 x 5 = 20
 5 x 5 = 25
 6 x 5 = 30
 7 x 5 = 35
 8 x 5 = 40
 9 x 5 = 45
10 x 5 = 50
"""