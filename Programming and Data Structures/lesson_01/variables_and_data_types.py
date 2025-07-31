# variables_and_data_types.py
# demonstrate variable declaration and check data types in Python

# declare variables 
name = "Sun" # string
age = 26 # int
height = 1.8  # float
male = True # bool

# checking data types 
print("Type of name: ", type(name)) # Output: <class 'str'>
print("Type of age: ", type(age)) # Output: <class 'int'>
print("Type of height: ", type(height)) # Output: <class 'float'>
print("Type of male: ", type(male)) # Output: <class 'bool'>

# constants
HOUR_PER_DAY = 24
day = 7
hours = day * HOUR_PER_DAY
print("Hours in", day, "days:", hours) 
#Output: Hours in 7 days: 168

