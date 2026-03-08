# if_else_statements.py
# Demonstrates double-selection (if-else)

# Get the number of items from the user
item_input = input("Enter the quantity: ")
item_count = int(item_input)

# Calculate the cost
if item_count <= 50:
    unit_price = 3
    postage = 10
    total_cost = unit_price * item_count + postage
else:
    unit_price = 2
    total_cost = unit_price * item_count

# Display the total cost
print("Total cost: ${0}".format(total_cost))