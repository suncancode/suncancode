# linked_list_basics.py
# Demonstrates linked list and node class

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Create nodes
node1 = Node(10)
node2 = Node(20)
node3 = Node(30)

# Link them
node1.next = node2
node2.next = node3

# Traverse and print
current = node1
while current is not None:
    print(current.data)
    current = current.next  # Output: 10 20 30