# date_handling.py
# Demonstrate how to  handle dates in Python using datetime

import datetime

# Getting current date (can use now() or date())
today_date = datetime.date.today() # call today() function to get current time
# Display current date
print("Today's date:", today_date)
print("Type of today_date:", type(today_date)) # output: <class 'datetime'>

# Getting user input for DOB
user_input = input("Enter your  DOB (DD/MM/YYYY): ")
try:
    # Ask user to enter their DOB
    """
    How to use "strptime" (string parse time): 
    call datetime.datetime.strptime(string, format)
    or datetime.date.strptime(string, format) (if just need the day)
    Input parameter
    - string:  eg. 30/06/2020
    - format: eg. %d (day), %m(month), %Y(year), %H(hour), %M(minute), %S(second),...
    Return:
    - datetime.datetime
    - datetime.date (if using .date())

    How to use "strftime" (string format time)
    function  strftime(format) turn "datetime.datetime" or "datetime.date" into input format
    """
    dob = datetime.datetime.strptime(user_input, "%d/%m/%Y").date()
    # Display DOB in 2 ways
    print("Your DOB is:", dob.strftime("%d/%b/%Y")) # output: ...30/Jun/2020
    print("Your DOB is:", dob.strftime("%d-%m-%Y")) # output: ...30-06-2020
except ValueError:
    print("Invalid input!")