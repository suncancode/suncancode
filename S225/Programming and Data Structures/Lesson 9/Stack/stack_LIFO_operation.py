# Practice with Stack operations and LIFO behavior

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def top(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        return str(self.items)

# Test the LIFO behavior
if __name__ == "__main__":
    # Create a new stack
    s = Stack()

    # Push items in order
    s.push(1)
    s.push(2)
    s.push(3)
    print("Stack after pushing 1, 2, 3:", s)  # Output: [1, 2, 3]

    # Pop items to demonstrate LIFO
    item1 = s.pop()
    print("Popped item:", item1)  # Output: 3
    item2 = s.pop()
    print("Popped item:", item2)  # Output: 2
    print("Stack after popping 2 items:", s)  # Output: [1]

    # Push and pop more items
    s.push(4)
    s.push(5)
    print("Stack after pushing 4, 5:", s)  # Output: [1, 4, 5]
    item3 = s.pop()
    print("Popped item:", item3)  # Output: 5
    print("Final stack:", s)  # Output: [1, 4]