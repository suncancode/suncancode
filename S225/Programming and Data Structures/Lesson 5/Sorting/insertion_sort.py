# insertion_sort.py
# Demonstrates Insertion sort algorithm

def insertion_sort(intList):
    n = len(intList)
    for i in range(1, n):
        j = i
        while j > 0 and intList[j] < intList[j - 1]:
            # Swap
            intList[j], intList[j - 1] = intList[j - 1], intList[j]
            """
            temp = intList[j]
            intList[j] = intList[j - 1]
            intList[j - 1] = temp   
            """
            j -= 1
    return intList

# Example from lecture
list_example = [60, 10, 90, 50, 100, 80, 70, 30, 40, 20]
print("Original list:", list_example)
sorted_list = insertion_sort(list_example)
print("Sorted list:", sorted_list)