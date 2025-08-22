# for_loop_pattern.py
# Demonstrate nested for-loops for patterns and sum calculation

# Sum of number from 1 to 10
result = 0
for i in range(1, 11):
    result += i
print("Sum of 1 to 10:", result)

# Consecutive numbers with comma and period
print()
print("Consecutive number:")
for i in range(0, 11):
    print(i, end = "")
    if i < 10:
        print(", ", end ="")
    else:
        print(". ")

# Number pattern (decreasing numbers)
print()
print("Number pattern:")
for i in range(1, 6):
    start_num = 2 * i
    for j in range(0, start_num):
        print(start_num - j, end = " ")
    print()
