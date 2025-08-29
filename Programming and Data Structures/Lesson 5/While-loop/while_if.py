# while_if.py
# Demonstrates while with if for Friend of 10 and even numbers

# Friend of 10 table
i = 0  # Initialization
while i <= 10:  # Conditional
    print("{0:>2} + {1:>2} = {2:>2}".format(i, 10 - i, 10))
    i = i + 1  # Post-loop update

# Even numbers with comma and period
i = 0  # Initialization
while i <= 10:  # Conditional
    print(i, end="")
    if i < 10:
        trailing = ", "
    else:
        trailing = "."
    print(trailing, end="")
    i = i + 2  # Post-loop update