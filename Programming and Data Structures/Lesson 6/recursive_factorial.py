# recursive_factorial.py
# Demonstrates recursive function for factorial

# Recursive factorial function
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Print 1! to 9!
for i in range(1, 10):
    print("{0}! = {1}".format(i, factorial(i)))