# expanding_word.py
# Demonstrates function to expand word by multiplicity

def expand(word, multiplicity):
    result = ""
    for i in range(0, len(word)):
        letter = word[i]
        result += letter * multiplicity
    return result

# Test
word = input("Enter a word: ")
multiplicity = int(input("Enter expand factor: "))
new_word = expand(word, multiplicity)
print("Here you go: " + new_word)