# Practice with dictionary for problem solving (count word frequency)

# Sample sentence
sentence = "the cat and the dog and the frog"

# Create an empty dictionary to store word counts
word_count = {}

# Split sentence into words and count frequency
'''
The split() method is used to divide a string into a list of substrings based on a specified separator.
Syntax: str.split(sep=None, maxsplit=-1)

Parameters:
- sep: (optional) The delimiter string. If not provided, whitespace is used by default.
- maxsplit: (optional) Maximum number of splits. Default is -1, which means "all possible splits".

Examples:
"apple,banana,cherry".split(',') → ['apple', 'banana', 'cherry']
'''
words = sentence.split()
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

# Print the word frequency
print("Word frequency:", word_count) # Output: {'the': 3, 'cat': 1, 'and': 2, 'dog': 1, 'frog': 1}

# Find the most frequent word
'''
In this line, word_count.get is passed as a function reference to the key argument of max().
It is not called directly (no parentheses), but max() will internally call word_count.get(key) for each key.
This allows max() to compare dictionary values and return the key with the highest value.

Example:
word_count = {'apple': 3, 'banana': 5, 'cherry': 2}
most_frequent = max(word_count, key=word_count.get) → 'banana'
'''
most_frequent = max(word_count, key=word_count.get)
print("Most frequent word:", most_frequent)  # Output: the