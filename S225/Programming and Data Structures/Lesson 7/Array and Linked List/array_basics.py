# array_basics.py
# Demonstrates array basics, access, insert, delete

# Array example
intList = [10, 20, 30, 40, 50]

# Access
print(intList[2])  # 30

# Modify
intList[2] = 35
print(intList[2])  # 35

# Insert at position 2
value = 25
position = 2
for i in range(len(intList) - 1, position - 1, -1):
    intList[i] = intList[i - 1]
intList[position] = value  # Assume array has space or use list.append first
print(intList)  # [10, 20, 25, 30, 40, 50] (if extended)

# Delete at position 1
position = 1
for i in range(position, len(intList) - 1):
    intList[i] = intList[i + 1]
intList.pop()  # Remove last (now duplicate)
print(intList)  # [10, 30, 40, 50]