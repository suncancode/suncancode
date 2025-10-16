# Practice with binary search tree insertion

class BinarySearchTreeNode:
    def __init__(self, value):
        """Initialize a BST node with a value and left/right children."""
        self.value = value
        self.left = None
        self.right = None

    def insert(self, value):
        """Insert a new value into the BST"""
        if value < self.value:
            if self.left is None:
                self.left = BinarySearchTreeNode(value)
            else:
                self.left.insert(value)
        else:
            if self.right is None:
                self.right = BinarySearchTreeNode(value)
            else:
                self.right.insert(value)

    def __str__(self, level=0):
        """Return a string representation of the BST with indentation"""
        result = "   " * level + str(self.value) + "\n"
        if self.left:
            result += self.left.__str__(level + 1)
        if self.right:
            result += self.right.__str__(level + 1)
        return result
    
# Create and populate a BST
if __name__ == "__main__":
    # Create root node
    root = BinarySearchTreeNode(10)

    # Insert values
    root.insert(5)
    root.insert(15)
    root.insert(3)
    root.insert(7)

    # Print the BST structure
    print("Binary Search Tree representation:")
    print(root)