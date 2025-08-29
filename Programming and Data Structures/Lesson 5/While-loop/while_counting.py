# while_counting.py
# Demonstrates counting backward and times table with while

# Going backward (9 to 0)
i = 9  # Initialization
while i >= 0:  # Conditional
    print(i)
    i = i - 1  # Post-loop update

# Times table example
i = 1  # Initialization
while i < 10:  # Conditional
    print("{0} x {1} = {2}".format(i, 5, 5 * i))
    i = i + 1  # Post-loop update