# Practice with Stack to reverse a list

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0

# Function to reverse a list using a stack
def reverse_list(input_list):
    # Create a new stack
    s = Stack()
    
    # Push all items to stack
    for item in input_list:
        s.push(item)
    
    # Pop items to create reversed list
    reversed_list = []
    while not s.is_empty():
        reversed_list.append(s.pop())
    
    return reversed_list

# Test the reverse function
if __name__ == "__main__":
    # Original list
    original = ["dog", "cat", "frog", "emu"]
    print("Original list:", original)  # Output: ['dog', 'cat', 'frog', 'emu']

    # Reverse the list
    reversed_result = reverse_list(original)
    print("Reversed list:", reversed_result)  # Output: ['emu', 'frog', 'cat', 'dog']