# Practice with Queue implementation

class Queue:
    def __init__(self):
        """Initialize an empty queue using a list"""
        self.items = []

    def enqueue(self, item):
        """Add an item to the end of the queue"""
        self.items.append(item)

    def dequeue(self):
        """
        Remove and return the item at the front of the queue
        Return None if the queue is empty
        """
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def front(self):
        """
        Return the item at the front of the queue without removing it
        Return None if the queue is empty
        """
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        """Return True if the queue is empty, False otherwise"""
        return len(self.items) == 0
    
    def __str__(self):
        """Return a string representation of the queue"""
        return str(self.items)
    
# Test the Queue
if __name__ == "__main__":
    # Create a new queue
    q = Queue()

    # Enqueue some items
    q.enqueue("apple")
    q.enqueue("banana")
    q.enqueue("cherry")
    print("Queue after enqueuing:", q)  # Output: ['apple', 'banana', 'cherry']

    # Check front item
    print("Front item:", q.front())  # Output: apple

    # Dequeue an item
    dequeued_item = q.dequeue()
    print("Dequeued item:", dequeued_item)  # Output: apple
    print("Queue after dequeuing:", q)  # Output: ['banana', 'cherry']

    # Check empty queue
    empty_queue = Queue()
    print("Empty queue dequeue:", empty_queue.dequeue())  # Output: None
    
