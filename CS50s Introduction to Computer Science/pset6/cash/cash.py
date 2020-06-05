from cs50 import get_float

while True:
    changeOwed = get_float('Change owed:\n')
    if changeOwed < 0:
        changeOwed = input('Change owed:\n')
    else:
        break
# Multiply everything by 100 so we can use Ints
changeOwed = int(changeOwed * 100)

# Define coins (* 100)
coins = {
    "quarter": 25,
    "dime": 10,
    "nickel": 5,
    "penny": 1
}

curAmount = 0
coinsAmount = 0

# Start adding coins
while curAmount != changeOwed:
    curAmount += coins['quarter']
    if curAmount > changeOwed:
        curAmount -= coins['quarter']
    else:
        coinsAmount += 1
        continue

    curAmount += coins['dime']
    if curAmount > changeOwed:
        curAmount -= coins['dime']
    else:
        coinsAmount += 1
        continue

    curAmount += coins['nickel']
    if curAmount > changeOwed:
        curAmount -= coins['nickel']
    else:
        coinsAmount += 1
        continue

    curAmount += coins['penny']
    if curAmount > changeOwed:
        curAmount -= coins['penny']
    else:
        coinsAmount += 1
        continue

    if curAmount == changeOwed:
        break

print(coinsAmount)