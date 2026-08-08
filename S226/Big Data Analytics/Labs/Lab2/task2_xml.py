"""
Task 2 - Semi-structured data: XML student records
CSCI446/946 Big Data Analytics - Lab 1
"""

import os
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

# ---- Đường dẫn tới thư mục chứa dataset ----
DATA_DIR = r"D:\sun\WOLLONGONG\S226\CSCI946 - Big Data Analytics\Lab\W2\Lab1-Released\CSCI446_946_Week2_Lab_SP_2026_Datasets"

# 2.1 Load and inspect the XML file
tree = ET.parse(os.path.join(DATA_DIR, "students.xml"))
root = tree.getroot()

print("Root tag:", root.tag)
print("Number of students:", len(root))

for student in root:
    print(student.get("id"), student.find("name").text,
          student.find("program").text, student.find("mark").text)

# 2.2 Convert selected XML elements into a DataFrame
records = []
for student in root.findall("student"):
    records.append({
        "student_id": student.get("id"),
        "name": student.find("name").text,
        "program": student.find("program").text,
        "year": int(student.find("year").text),
        "mark": int(student.find("mark").text)
    })

students = pd.DataFrame(records)
print(students)

# --- Thông tin hỗ trợ trả lời câu hỏi ---
top_student = students.loc[students["mark"].idxmax()]
print("\nStudent with the highest mark:")
print(top_student)

students.plot(x="name", y="mark", kind="bar",
              legend=False, title="Student Marks")
plt.ylabel("Mark")
plt.tight_layout()
plt.show()

"""
Questions to answer:
1. What is the root tag of the XML document?
2. What is the difference between the student id attribute and the name element?
3. Which student has the highest mark?
"""
