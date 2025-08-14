# multiple_selection.py
# Demonstrates multiple selection using if-elif-else statements

# Get the mark from the user
mark = int(input("Please input mark: "))

# Determine the grade based on mark
if mark >= 80:
    grade = "A"
elif mark >= 60:
    grade = "B"
elif mark >= 40:
    grade = "C"
else:
    grade = "D"

# Display the mark and grade
print("Mark {0}, Grade {1}".format(mark, grade))