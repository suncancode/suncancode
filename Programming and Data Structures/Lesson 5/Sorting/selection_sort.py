# selection_sort.py
# Demonstrates Selection sort algorithm

def selection_sort(int_list):
    n = len(int_list)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if int_list[j] < int_list[min_index]:
                min_index = j
        # Swap
        int_list[i], int_list[min_index] = int_list[min_index], int_list[i]
    return int_list

# Example list
list_example = [60, 10, 90, 50, 100, 80, 70, 30, 40, 20]
print("Original list:", list_example)
sorted_list = selection_sort(list_example)
print("Sorted list:", sorted_list)