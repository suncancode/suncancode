# Practice with dictionary for grouping data

# Create a dictionary to store student information
student = {
    "first_name": "Emma",
    "last_name": "Wilson",
    "student_id": "S12345",
    "major": "Computer Science"
}

# Access and print grouped data
print("Student full name:", student["first_name"] + " " + student["last_name"])
print("Student ID:", student["student_id"])
print("Major:", student["major"])

# Add a new key-value pair to the dictionary
student["gpa"] = 3.9
print("Updated student info:", student) # Output: {'first_name': 'Emma', 'last_name': 'Wilson', 'student_id': 'S12345', 'major': 'Computer Science', 'gpa': 3.8}