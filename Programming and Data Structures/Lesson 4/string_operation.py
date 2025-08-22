# string_operation.py
# Demonstrate string methods: upper/lower, find, len, indexing

name = "Sunnie"

# Upper and lower case
print("Uppercase:", name.upper())
print("Lowercase:", name.lower())

# Find substring
"""
find() returns the first index if found, otherwise, it return -1 if not found
Index 0 means the first character.
"""
index = name.find("un")
print("Index of 'un':", index)
index = name.find("ni")
print("Index of 'ni':", index)
index = name.find("ie")
print("Index of 'ie':", index)
index = name.find("Sunnie")
print("Index of 'Sunnie':", index)

# Length
print("Length:", len(name))

# Indexing
"""
last index?   
Answer: len(greeting) - 1
"""
print("First character:", name[0])
print("Last character:", name[-1])

# Slicing
"""
[i:j] gives substring from index i up to index (j-1), so altogether, there are (j-i) characters

[i:] gives substring from index i up to the end

[:j] is the same as [0:j] gives substring from index 0 up to index (j-1), so altogether, there are j characters 
"""
print("First 3 character:", name[0: 3])
print("Reversed:", name[::-1])

# In operator
print("'unn' in name:", "unn" in name)
print("'nnn' in name:", "nnn" in name)
