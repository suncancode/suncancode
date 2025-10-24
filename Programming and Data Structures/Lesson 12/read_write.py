# Practice with reading and writing text file

# Write to a text file
silly_file_path = "silly.txt"

with open(silly_file_path, "w") as silly_file:
    silly_file.write("Hi")
    silly_file.write("I am Sun")
    silly_file.write("Would you like to say hi?")

# Read text file using while-loop
with open(silly_file_path) as silly_file:
    while True:
        line = silly_file.read()
        if line == "":
            break
        print(line, end="")

# Read text file using for-loop with strip
with open(silly_file_path) as silly_file:
    for line in silly_file:
        print(line.strip())