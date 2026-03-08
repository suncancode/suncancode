# Practice with writing times table to text file

# Ask user for input
user_input = input("Enter a number to generate times table: ")
number = int(user_input)
file_path = input("Enter output file path: ")

# Write times table to file 
with open(file_path, "w") as timestable_file:
    for i in range(1, 10):
        timestable_file.write("{0} x {1} = {2}\n".format(number, i, number * i))