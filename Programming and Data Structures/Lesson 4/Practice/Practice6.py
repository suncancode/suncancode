# Get user input
n = int(input("Enter an integer: "))

# Print even number from 2 to 2*n in group of 4
for i in range(1, n + 1):
    number = 2 * i
    print(number, end="")
    # Determine trailing punctuation
    if i % 4 == 0 and i != n:
        print(";", end="")
    elif i < n:
        print(",", end="")
    else:
        print(".")
