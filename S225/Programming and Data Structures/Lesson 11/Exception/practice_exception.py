# Advanced practice with exception handling (file processing with multiple check)

# Define a custom exception class
class FileProcessingError(Exception):
    """Custom exception for file processing errors."""
    pass

def process_file(filename):
    # Attempt to open and process a file
    try:
        with open(filename, 'r') as file:
            content = file.read()
            numbers = content.split()

            # Validate that all entries are numbers
            for num in numbers:
                if not num.isdigit():
                    raise FileProcessingError("File contains non-numberic data.")
                
                value = int(num)
                if value < 0:
                    raise ValueError("Negarive numbers are not allowed.")
                
            print("File content processed successfully:", numbers)
    except FileNotFoundError:
        print("Error: File not found.")
    except FileProcessingError as e:
        print("Error:", e)
    except ValueError as e:
        print("Error:", e)

# Test the function
if __name__ == "__main__":
    # Assuming a file 'numbers.txt' exists with content "1 2 3"
    process_file("numbers.txt")  # Output depends on file content
    
    # Test with non-existent file
    process_file("nonexistent.txt")  # Output: Error: File not found.