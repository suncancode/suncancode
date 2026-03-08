# Practice with Queue operations and FIFO behavior

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def front(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        return str(self.items)

# Test the FIFO behavior
if __name__ == "__main__":
    # Create a new queue
    q = Queue()

    # Enqueue items in order
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    print("Queue after enqueuing 1, 2, 3:", q)  # Output: [1, 2, 3]

    # Dequeue items to demonstrate FIFO
    item1 = q.dequeue()
    print("Dequeued item:", item1)  # Output: 1
    item2 = q.dequeue()
    print("Dequeued item:", item2)  # Output: 2
    print("Queue after dequeuing 2 items:", q)  # Output: [3]

    # Enqueue and dequeue more items
    q.enqueue(4)
    q.enqueue(5)
    print("Queue after enqueuing 4, 5:", q)  # Output: [3, 4, 5]
    item3 = q.dequeue()
    print("Dequeued item:", item3)  # Output: 3
    print("Final queue:", q)  # Output: [4, 5]