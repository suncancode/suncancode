# Practice with basic tree representation (HTML structure)

class TreeNode:
    def __init__(self, value):
        """Initialize a tree node with a value and empty list of children"""
        self.value = value
        self.children = []

    def add_child(self, child):
        """Add a child node to the current node"""
        self.children.append(child)

    def __str__(self, level=0):
        """Return a string representation of the tree with indentation"""
        result = " " * level + str(self.value) + "\n"
        for child in self.children:
            result += child.__str__(level + 1)
        return result
    
# Create a tree representing the HTML structure
if __name__ == "__main__":
    # Root node (html)
    html = TreeNode("<html>")

    # Add head and body as children
    head = TreeNode("<head>")
    body = TreeNode("<body>")
    html.add_child(head)
    html.add_child(body)

    # Add title to head 
    head.add_child(TreeNode("<title>FIFA</title>"))

    # Add h1 and ul to body
    body.add_child(TreeNode("<h1>Group A</h1>"))
    ul = TreeNode("<ul>")
    body.add_child(ul)

    # Add list items to ul
    ul.add_child(TreeNode("<li>Vietnam</li>"))
    ul.add_child(TreeNode("<li>China</li>"))
    ul.add_child(TreeNode("<li>Laos</li>"))
    ul.add_child(TreeNode("<li>Singapore</li>"))

    # Print the tree structure
    print("Tree representation of HTML")
    print(html)