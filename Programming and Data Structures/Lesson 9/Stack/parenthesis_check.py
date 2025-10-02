def math_expression_checking(expression):
    # Dictionary to match opening and closing brackets
    pairs = {')': '(', '}': '{', ']': '['}
    stack = []

    for char in expression:
        if char in pairs.values():  # Opening brackets
            stack.append(char)
        elif char in pairs:         # Closing brackets
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()

    return len(stack) == 0
