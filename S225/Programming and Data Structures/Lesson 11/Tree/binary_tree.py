# Practice with binary tree creation

class BinaryTreeNode:
    def __init__(self, value):
        """Initialize a binary tree node with a value and left/right children."""
        self.value = value
        self.left = None
        self.right = None

    def __str__(self, level=0):
        """Return a string representation of the binary tree with indentation."""
        result = "  " * level + str(self.value) + "\n"
        if self.left:
            result += self.left.__str__(level + 1)
        if self.right:
            result += self.right.__str__(level + 1)
        return result

# Create a binary tree
if __name__ == "__main__":
    # Create root node
    root = BinaryTreeNode("A")

    # Add left and right children
    root.left = BinaryTreeNode("B")
    root.right = BinaryTreeNode("C")

    # Add grandchildren
    root.left.left = BinaryTreeNode("D")
    root.left.right = BinaryTreeNode("E")
    root.right.left = BinaryTreeNode("F")

    # Print the binary tree structure
    print("Binary Tree representation:")
    print(root)