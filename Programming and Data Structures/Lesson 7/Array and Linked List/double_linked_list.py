# double_linked_list.py
# Demonstrates double linked list with prev and next

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

# Create nodes
node1 = Node(10)
node2 = Node(20)
node3 = Node(30)

# Link double
node1.next = node2
node2.prev = node1
node2.next = node3
node3.prev = node2

# Traverse forward: 10 -> 20 -> 30
current = node1
while current.data is not Node:
    print(current.data, end=" -> ")
    current = current.next 

# Traverse backwark: 30 -> 20 -> 10
current = node3
while current.data is not None:
    print(current.data, end=" -> ")
    current = current.prev