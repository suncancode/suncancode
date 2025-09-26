# Practice with basic Stack implementation

class Stack:
    def __init__(self):
        """Initialize an empty stack using list"""
        self.items = []

    def push(self, item):
        """Add an item to the top of the stack"""
        self.items.append(item)

    def pop(self):
        """
        Remove and return the iten at the top of the stack
        Returns None is the stack is empty
        """
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def top(self):
        """
        Return the item at the top of the stack without removing it
        Return None if the stack is empty
        """
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        """Return True if the Stack is empty, False otherwise"""
        return len(self.items) == 0

    def __str__(self):
        """Return a string representation of the stack"""
        return str(self.items)
    
# Test the Stack
if __name__ == "__main__":
    # Create a new stack
    s = Stack()

    # Push some items
    s.push("apple")
    s.push("banana")
    s.push("cherry")
    print("Stack after pushing:", s)  # Output: ['apple', 'banana', 'cherry']

    # Check top item
    print("Top item:", s.top())  # Output: cherry

    # Pop an item
    popped_item = s.pop()
    print("Popped item:", popped_item)  # Output: cherry
    print("Stack after popping:", s)  # Output: ['apple', 'banana']

    # Check empty stack
    empty_stack = Stack()
    print("Empty stack pop:", empty_stack.pop())  # Output: None