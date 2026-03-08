# Practice with Queue to simulate order processing

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
    
# Function to process orders
def process_orders(order_queue):
    while not order_queue.is_empty():
        order = order_queue.dequeue()
        print(f"Processing order: {order}")

# Main
if __name__ == "__main__":
    # Create a new queue for orders
    order_queue =  Queue()

    # Enqueue some orders
    order_queue.enqueue("Order #1: 2 pens")
    order_queue.enqueue("Order #2: 1 notebook")
    order_queue.enqueue("Order #3: 3 pencils")
    print("Order queue:", order_queue)  # Output: ['Order #1: 2 pens', 'Order #2: 1 notebook', 'Order #3: 3 pencils']

    # Process the orders
    process_orders(order_queue)
    print("Queue after processing:", order_queue)  # Output: []