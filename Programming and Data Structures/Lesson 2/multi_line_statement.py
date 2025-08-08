# multi_line_statement.py
# Demonstrates multi-line code statements in Python

# Valid multi-line statement using string concatenation
"""
 Line continuation is automatic when the split comes while a 
statement is inside parenthesis  ( , brackets  [  or braces  {   
"""
subject_code = "CSIT881"
subject_grade = "HD"
subject_mark = 100
result = (
    "Subject result: " + 
    subject_code + 
    subject_grade + 
    " grade " + 
    str(subject_mark)
)

print(result)  # Output: Subject result: CSIT881 grade 100

"""
 Use the backslash   \  to indicate that a statement is 
continued on the next line.

Example: 
subject_code = "CSCI111"
 subject_mark = 80
 subject_grade = "D"
 result = "Subject result: " \
  + subject_code \
  + " mark " + str(subject_mark) \
  + " grade " + subject_grade
 print(result)
"""

# Example of incorrect concatenation causing NameError
try:
    subject_code = "CSIT881"
    subject_mark = 100
    result = "Subject result: " + subject_code + " mark " + str(subject_mark) + " grade " + subject_grade
    print(result)
except NameError:
    print("Error: Variable 'subject_grade' is not defined.")