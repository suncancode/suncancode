# parenthesis_check.py
# Demonstrates Stack for parenthesis checking

def check_parenthesis(expression):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}
    for char in expression:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack.pop() != pairs[char]:
                return False
    return len(stack) == 0

# Test
expression = "4 * {z - [(a+b) * c]}"
print("Expression:", expression)
print("Valid:", check_parenthesis(expression))  # True

expression = "4 * {z - [(a+b) * c}"
print("Expression:", expression)
print("Valid:", check_parenthesis(expression))  # False