# Declare constant 
ADULT_UNIT_PRICE = 100
CHILD_UNIT_PRICE = 60
FUEL_SURCHARGE_PRICE = 50

# Get user input 
adult_num = int(input("How many adult passengers ($100 each): "))
child_num = int(input("How many child passengers ($100 each): "))

# Initialize variable for baggage
baggage_price = 0
# Logic to handle request to add baggage
baggage_request = input("Add baggage (Y)es (N)o: ")
if baggage_request.upper() == "Y":
    baggage_num = int(input("How many bags do you have (1) 15kg for $53.13 (2) 30 kg for $99.24: "))
    if baggage_num == 1:
        baggage_price = 53.13
    elif baggage_num == 2:
        baggage_price = 99.24

# Calculate total price
total_price = (
    adult_num * ADULT_UNIT_PRICE 
    + child_num * CHILD_UNIT_PRICE 
    + baggage_price
    + FUEL_SURCHARGE_PRICE
)

# Displaying ticket cost message
print(f"Your ticket costs ${total_price:.2f} (including Fuel Surcharge ${FUEL_SURCHARGE_PRICE})")

