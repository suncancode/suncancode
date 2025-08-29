# Get user input
start_num = int(input("Enter the starting integer: "))
end_num = int(input("Enter the ending integer: "))

# Display table
# Header
print(f"{"Num":<10}{"Double":<10}{"Triple":>10}")
# Using for-loop to display each row from starting number to ending number
for i in range(start_num, end_num + 1):
    print(f"{i:<10}{i * 2:<10}{i * 3:>10}")
