# Get user input
pnum = int(input(" Enter the number of puppies: "))
knum = int(input(" Enter the number of kitties: "))

# Logic for displaying number of animals
if pnum == 1 and knum == 1:
    print(f"You have adopted {pnum} puppy and {knum} kitty.")
elif pnum > 1 and knum ==  1:
    print(f"You have adopted {pnum} puppies and {knum} kitty.")
elif pnum > 1 and knum > 1:
    print(f"You have adopted {pnum} puppies and {knum} kitties.")