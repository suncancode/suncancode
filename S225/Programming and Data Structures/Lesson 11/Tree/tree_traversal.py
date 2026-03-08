# Advanced practice with tree traversal (pre-order)

class BinaryTreeNode:
    def __init__(self, value):
        """Initialize a binary tree node with a value and left/right children."""
        self.value = value
        self.left = None
        self.right = None

    def pre_order(self):
        """Perform pre-order traversal (root, left, right) and return the list of values."""
        result = [self.value]
        if self.left:
            result.extend(self.left.pre_order())
        if self.right:
            result.extend(self.right.pre_order())
        return result
    
    def in_order(self):
        """Perform in-order traversal (left, root, right)."""
        result = []
        if self.left:
            result.extend(self.left.in_order())
        result.append(self.value)
        if self.right:
            result.extend(self.right.in_order())
        return result

    def post_order(self):
        """Perform post-order traversal (left, right, root)."""
        result = []
        if self.left:
            result.extend(self.left.post_order())
        if self.right:
            result.extend(self.right.post_order())
        result.append(self.value)
        return result

    def level_order(self):
        """Perform level-order traversal using a queue."""
        result = []
        queue = deque([self])
        while queue:
            node = queue.popleft()
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def __str__(self, level=0):
        """Return a string representation of the binary tree with indentation."""
        result = "  " * level + str(self.value) + "\n"
        if self.left:
            result += self.left.__str__(level + 1)
        if self.right:
            result += self.right.__str__(level + 1)
        return result

# Create a binary tree for traversal
if __name__ == "__main__":
    # Create root node
    root = BinaryTreeNode(1)

    # Add left and right children
    root.left = BinaryTreeNode(2)
    root.right = BinaryTreeNode(3)

    # Add grandchildren
    root.left.left = BinaryTreeNode(4)
    root.left.right = BinaryTreeNode(5)
    root.right.left = BinaryTreeNode(6)

    # Perform pre-order traversal
    traversal_result = root.pre_order()
    print("Pre-order traversal:", traversal_result)  # Output: [1, 2, 4, 5, 3, 6]
    print("Binary Tree representation:")
    print(root)