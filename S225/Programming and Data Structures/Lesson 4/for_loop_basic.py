# for_loop_basics.py
# Demonstrates basic for-loop with range()

# Print numbers 0 to 9
print("Numbers 0 to 9:")
for i in range(0, 10):
    print(i)

print()

# Print times table based on user input
num = int(input("Enter a number for times table: "))
print(f"Times table for {num}:")
for i in range(0, 10):
    print("{0} x {1} = {2}".format(i, num, i * num))

print()

# Friend of 10 table with right alignment
print("Friend of 10 table:")
for i in range(0, 11):
    print("{0:^3} + {1:^3} = {2:>3}".format(i, 10 - i, 10))