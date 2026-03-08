# random_function.py
# Demonstrates random.randint for dice simulation

import random

for i in range(0, 10):
    random_number = random.randint(1, 6)
    print("Dice result: {0}".format(random_number))