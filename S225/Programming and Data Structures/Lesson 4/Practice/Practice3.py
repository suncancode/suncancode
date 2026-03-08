# Get user input
text =  input("Enter a string: ")
start_letter = input("Enter the starting letter: ")
end_letter = input("Enter the endinng letter: ")

# Find position of starting and ending letter in user input
start_index = text.find(start_letter) 
end_index = text.find(end_letter) 

# Logic to display string
if start_index == -1 and end_index == -1:
    print("Both letters are not found.")
elif start_index == -1 and  end_index > 0:
    for i in range(0, end_index + 1):
        print(text[i], end="")
        if i < end_index:
            print("-", end="")
        else:
            print(".")
elif start_index > 0 and end_index == -1:
    for i in range(start_index, len(text)):
        print(text[i], end="")
        if i < len(text) - 1:
            print("-", end="")
        else:
            print(".")
elif start_index > 0 and end_index > 0:
    for i in range(start_index, end_index + 1):
        print(text[i], end="")
        if i < end_index:
            print("-", end="")
        else:
            print(".")