# Practice with manual raising an exception when a condition is not met

def check_age(age):
    # Check if age is negative
    if age < 0:
        raise ValueError("Age cannot be negative")
    print("Age is valid:", age)

# Test the function
if __name__ == "__main__":
    try:
        check_age(25)  # Output: Age is valid: 25
        check_age(-5)  # Raises ValueError
    except ValueError as e:
        print("Error:", e)