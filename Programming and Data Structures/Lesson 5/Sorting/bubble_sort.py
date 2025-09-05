# bubble_sort.py
# Demonstrates Bubble sort

def bubble_sort(intList):
    n = len(intList)
    for i in range(n):
        for j in range(0, n - i - 1):
            if intList[j] > intList[j + 1]:
                # Swap
                intList[j], intList[j + 1] = intList[j + 1], intList[j]
    return intList

# Example list
list_example = [60, 10, 90, 50, 100, 80, 70, 30, 40, 20]
print("Original list:", list_example)
sorted_list = bubble_sort(list_example)
print("Sorted list:", sorted_list)