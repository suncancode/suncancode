# Practice with reading and writing CSV file (subject data)

import csv

# Write to CSV file
subject_file_path = "subject.csv"

with open(subject_file_path, "w") as subject_file:
    field_name_list = ["code", "name", "cp"]
    writer = csv.DictWriter(subject_file, fieldnames=field_name_list)
    writer.writeheader()
    writer.writerow({"code": "CSIT881", "name": "Programming", "cp": 6})
    writer.writerow({"code": "CSIT882", "name": "Web", "cp": 6})
    writer.writerow({"code": "CSIT884", "name": "Database", "cp": 6})

# Read from the CSV file
with open(subject_file_path) as subject_file:
    reader = csv.DictReader(subject_file)
    for row in reader:
        subject_code = row.get("code")
        subject_name = row.get("name")
        cp = row.get("cp")
        print("{0:<10}|{1:<10}|{2:<10}".format(subject_code, subject_name, cp))