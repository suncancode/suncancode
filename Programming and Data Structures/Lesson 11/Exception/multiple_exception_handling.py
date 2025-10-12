# Practice with multiple exception handling

def divide_numbers(a, b):
    # Attempt to divide 2 numbers
    try:
        result = a / b
        print("Result:", result)
    except ZeroDivisionError:
        # Handle division by zero
        print("Error: Division by zero is not allowed.")
    except TypeError:
        # Handle invalid type for division
        print("Error: Please provide valid numbers.")

# Test the function
if __name__ == "__main__":
    divide_numbers(10, 2)  # Output: Result: 5.0
    divide_numbers(10, 0)  # Output: Error: Division by zero is not allowed.
    divide_numbers(10, "2")  # Output: Error: Please provide valid numbers.