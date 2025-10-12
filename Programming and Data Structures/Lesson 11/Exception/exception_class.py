# Practice defining a custom exception class and using it in a program

# Define a custom exception class
class CustomValueError(Exception):
    """Custom exception for invalid values."""
    pass

def validate_score(score):
    # Validate if score is between 0 and 100
    if not (0 <= score <= 100):
        raise CustomValueError("Score must be between 0 and 100.")
    print("Score is valid:", score)

# Test the function 
if __name__ == "__main__":
    try:
        validate_score(85)
        validate_score(101)
    except CustomValueError as e:
        print("Error:", e)