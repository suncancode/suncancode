class TreeNode:
#{
    """
    Representing a tree node consisting of
    - datum: the datum stored at the node
    - left: reference to the left child node
    - right: reference to the right child node
    """   

    def __init__(self, datum, left=None, right=None):
    #{
        self.datum = datum
        self.left = left
        self.right = right
    #}

    def in_order(self):
        if self.left != None:
            self.left.in_order()
        print(self.datum)
        if self.right != None:
            self.right.in_order()

    def pre_order(self):
        print(self.datum)
        if self.left != None:
            self.left.pre_order()
        if self.right != None:
            self.right.pre_order()

    def post_order(self):
        if self.left != None:
            self.left.post_order()
        if self.right != None:
            self.right.post_order()
        print(self.datum)

#}

class MyBinaryTree:
#{
    """
    Implementation of a binary tree
    """ 

    def __init__(self):
    #{
        """
        Constructs an empty tree
        """
        self.root = None

    #}

    def print_in_order(self):
    #{
        """
        Use in-order traversal and print each tree node's datum
        """  
        if self.root != None:
            self.root.in_order()
    #}

    def print_pre_order(self):
    #{
        """
        Use pre-order traversal and print each tree node's datum
        """ 
        if self.root != None:
            self.root.pre_order()
    #}

    def print_post_order(self):
    #{
        """
        Use post-order traversal and print each tree node's datum
        """    
        if self.root != None:
            self.root.post_order()
    #}

#}

# Level 3
nodeI = TreeNode("I", None, None)
nodeJ = TreeNode("J", None, None)
nodeK = TreeNode("K", None, None)
nodeL = TreeNode("L", None, None)
nodeM = TreeNode("M", None, None)
# Level 2
nodeD = TreeNode("D", None, None)
nodeE = TreeNode("E", nodeI, nodeJ)
nodeF = TreeNode("F", nodeK, nodeL)
nodeH = TreeNode("H", nodeM, None)
# Level 1
nodeB = TreeNode("B", nodeD, nodeE)
nodeC = TreeNode("C", nodeF, nodeH)
# Level 0
nodeA = TreeNode("A", nodeB, nodeC)

myTreeObj = MyBinaryTree()
myTreeObj.root = nodeA

print("In_order:")
myTreeObj.print_in_order()
print("Pre-order:")
myTreeObj.print_pre_order()
print("Postorder:")
myTreeObj.print_post_order()