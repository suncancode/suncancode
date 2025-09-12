# linked_list_operations.py
# Demonstrates insert and delete in linked list

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Initialize list: 10 -> 20 -> 30
node1 = Node(10)
node2 = Node(20)
node3 = Node(30)
node1.next = node2
node2.next = node3

# Insert 15 between 10 and 20
new_node = Node(15)
new_node.next = node1.next # 15 -> 20
node1.next = new_node # 10 -> 15

# Print list 10 -> 15 -> 20 -> 30
current = node1
while current is not None:
    print(current.data, end=" -> ")
    current = current.next

# Delete 20: 10 -> 15 -> 30
node2 = new_node.next # 20 -> 20
new_node.next = node2.next # 15 -> 30

# Print list 10 -> 15 -> 30
current = node1
while current is not None:
    print(current.data, end=" -> ")
    current = current.next