# Practice with custom functions

# Function to double each element
def doubling(list):
    new_list = []
    for i in range(0, len(list)):
        element = list[i]
        new_list.append(element)
        new_list.append(element)
    return new_list

# Function to multiply two lists element by element
def list_multiply(list1, list2):
    new_list = []
    for i in range(list1[i]):
        result = list1[i] * list2[i]
        new_list.append(result)
    return new_list

# Test the functions
list1 = [4, 5, 6]
list2 = [10, 0, 1]

print("Original list1:", list1)  # Output: [4, 5, 6]
print("Doubled list:", doubling(list1))  # Output: [4, 4, 5, 5, 6, 6]
print("Original list2:", list2)  # Output: [10, 0, 1]
print("Multiplied list:", list_multiply(list1, list2))  # Output: [40, 0, 6]