from cs50 import get_int

while True:
    size = get_int('Please enter a size between 1 - 8:\n')
    if size < 0 or size > 8:
        size = input('Please enter a size between 1 - 8:\n')
    else:
        break
row = 1
for i in range(size):
    # First print out the spaces on the row
    for j in range(size - row):
        print(" ", end = "")
    # Then print out the hash marks for the left pyramid
    for k in range(row):
        print("#", end = "")
    # Then print the two spaces
    for i in [1, 2]:
        print(" ", end = "")
    # Lastly print out the hash marks for the right pyramid
    for m in range(row):
        print("#", end = "")
    row += 1
    print("\n", end = "")

