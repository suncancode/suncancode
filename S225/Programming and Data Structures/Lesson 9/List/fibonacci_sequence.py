# Practice with Fibonacci sequence

# Create an empty list for Fibonacci sequence
fibo_list = []

# Append first 2 numbers
fibo_list.append(0)
fibo_list.append(1)

# Generate next 8 number
for i in range(2, 10):
    fibo = fibo_list[i - 1] + fibo_list[i - 2]
    fibo_list.append(fibo)

print("First 10 Fibonacci numbers: ", fibo_list)