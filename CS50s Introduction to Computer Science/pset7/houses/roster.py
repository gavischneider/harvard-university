import csv
from sys import argv, exit
from cs50 import SQL

if len(argv) != 2:
    print("Error")
    exit(1)

open("students.db", "r").close()
db = SQL("sqlite:///students.db")

requestedHouse = str(argv[1])
list = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first;", requestedHouse)

for row in list:
    first = row["first"]
    middle = row["middle"]
    last = row["last"]
    birth = row["birth"]

    if middle == None:
        print(f"{first} {last}, born {str(birth)}")
    else:
        print(f"{first} {middle} {last}, born {str(birth)}")
