# Declare constant
PINK_LADY_PRICE = 4.99
FUJI_PRICE = 5.99
HAMLIN_PRICE = 2.99
MORO_PRICE = 3.99

# Get user input
apple_type = input("Which kind of apples would you like: (P)ink Lady 4.99/kilo (F)uji 5.99/kilo: ") 

# Declare variable for displaying reciept
apple_name = ""
apple_price = 0
# Calculate apple price based on type of apple
if apple_type.upper() == "P":
    apple_name = "Pink Lady"
    apple_weight = float(input("How many kilograms of apples would you like: "))
    apple_unit_price = PINK_LADY_PRICE
    apple_price = apple_weight * PINK_LADY_PRICE
elif apple_type.upper() == "F":
    apple_name = "Fuji"
    apple_weight = float(input("How many kilograms of apples would you like: "))
    apple_unit_price = FUJI_PRICE
    apple_price = apple_weight * FUJI_PRICE
else:
    apple_name = "-"
    apple_weight = 0
    apple_unit_price = 0
    apple_price = 0


orange_type = input("Which kind of oranges would you like: (H)amlin 2.99/kilo (M)oro 3.99/kilo: ")
# Declare variable for displaying reciept
orange_name = ""
orange_price = 0
# Calculate orange price based on type of orange
if orange_type.upper() == "H":
    orange_name = "Hamlin"
    orange_weight = float(input("How many kilograms of oranges would you like: "))
    orange_unit_price = HAMLIN_PRICE
    orange_price = orange_weight * HAMLIN_PRICE
elif orange_type.upper() == "M":
    orange_name = "Moro"
    orange_weight = float(input("How many kilograms of oranges would you like: "))
    orange_unit_price = MORO_PRICE
    orange_price = orange_weight * MORO_PRICE
else:
    orange_name = "-"
    orange_weight = 0
    orange_unit_price = 0
    orange_price = 0

# Calculate total price
total_price = apple_price + orange_price

# Displaying receipt
print(f"{"Item":>15}{"Weight":>15}{"Unit Price":>15}{"Price":>15}")
print(f"{apple_name:>15}{apple_weight:>15.2f}{apple_unit_price:>15.2f}{apple_price:>15.2f}")
print(f"{orange_name:>15}{orange_weight:>15.2f}{orange_unit_price:>15.2f}{orange_price:>15.2f}")
print(f"{"Total":>15}{"":>15}{"":>15}{total_price:>15.2f}")

    

