# Practice with list traversal and modification

# Create a list of numbers
random_numbers = [1, 2, 4, 5, 7, 8]

# Increase each item by 10 using for loop with index
for i in range(0, len(random_numbers)):
    random_numbers[i] = random_numbers[i] + 10
print("Numbers after increasing by 10: ", random_numbers)

# Create square numbers list
square_list = []
for i in range(0, 10):
    square_number = i * i
    square_list.append(square_number)
print("First 10 square numbers :", square_list)