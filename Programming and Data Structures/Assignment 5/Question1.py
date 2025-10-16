# Declare dictionary for items
items = {}

# Get user input for records
n = int(input("Enter number of records: "))
count_record = 0 

# Use while loop to add item to items dict
while count_record < n:
    name = input("Enter name: ")
    quantity = int(input("Enter quantity: "))
    quantity = max(quantity, 0) # Treat negative quantities as 0
    
    # Check if item is in items dict then add quantity
    if name in items:
        items[name] += quantity
    else:
        items[name] = quantity

    # Increament count
    count_record += 1

# Remove any items whose total quantity is 0
remove_list = []
for item in items:
    if items[item] == 0:
        remove_list.append(item) # Add item to remove
for item in remove_list:
    del items[item]

# Get user input for queries
q = int(input("\nEnter number of queries: "))
count_query = 0
total_unique_item = 0
total_quantity = 0

# Use while loop to display total number of each item in the dict
while count_query < q:
    name = input("Query name: ")

    # Check if item is in the dict
    if name in items:
        print("{0}: {1}".format(name, items[name]))
        total_unique_item += 1
        total_quantity += items[name]
    else:
        print("{0}: {1}".format(name, 0))

    # Increament count for query
    count_query += 1

print("\nTotal unique items:", total_unique_item)
print("Total quantity:", total_quantity)
