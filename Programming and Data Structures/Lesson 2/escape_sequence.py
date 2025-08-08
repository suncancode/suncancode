# escape_sequence.py
# Demonstrates escape sequences (\t, \") and fixing print errors

# Using tab (\t) and quote (\") escape sequences
print("\tName: \"Trung Duc\"")  # Output:     Name: "John Smith"
print("\tSN: \"1008389\"")  # Output:     SN: "2012345"
print("\tEnrollment record:")  # Output:     Enrollment record:
print("\t\tCSIT881")  # Output:         CSIT881

# Fixing printprint error
print("Welcome to Unimovies!")  # Corrected from printprint
print("Thursday July 30 at 7.15pm: Inside Out")  # Output: Thursday July 30 at 7.15pm: Inside Out

"""
Escape sequences and meanings
\\  : Backslash (\)
 \' : Single quote (')
 \" : Double quote (")
 \n : New line
 \t : Tab
"""

# Using escape sequence
print("Thursday July 30 at 7.15pm: \"Inside Out\"")  # Output: Thursday July 30 at 7.15pm: "Inside Out"

