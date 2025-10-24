# Practice with reading and writing CSV file (student data)

import csv

# Write to a CSV file
student_file_path = "student.csv"

with open(student_file_path, "w") as student_file:
    field_name_list = ["ID", "first_name", "last_name"]
    writer = csv.DictWriter(student_file, fieldnames=field_name_list)
    writer.writeheader()
    writer.writerow({"ID": "1111", "first_name": "Duc", "last_name": "Le"})
    writer.writerow({"ID": "2222", "first_name": "Khoi", "last_name": "Chu"})
    writer.writerow({"ID": "3333", "first_name": "Bach", "last_name": "Phan"})
    writer.writerow({"ID": "4444", "first_name": "Tung", "last_name": "Le"})

# Read from CSV file
with open(student_file_path) as student_file:
    reader = csv.DictReader(student_file)
    for row in reader:
        student_number = row.get("ID")
        fname = row.get("first_name")
        lname = row.get("last_name")
        print("{0:<10}|{1:<10}|{2:<10}".format(student_number, fname, lname))