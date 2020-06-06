import csv
from sys import argv, exit
from cs50 import SQL

if len(argv) != 2:
    print("Error")
    exit(1)

open("students.db", "w").close()
db = SQL("sqlite:///students.db")
db.execute("CREATE TABLE students(first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC);")

# Start going over each studen row from the file
with open(argv[1], 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        splitName = row['name'].split()
        #print(splitName)
        # Check if student has two or three names
        if len(splitName) == 3:
            first = splitName[0]
            middle = splitName[1]
            last = splitName[2]
        else:
            first = splitName[0]
            middle = None
            last = splitName[1]
        house = row['house']
        birth = row['birth']

        # Now enter the row into the db
        db.execute("INSERT INTO students(first, middle, last, house, birth) Values(?, ?, ?, ?, ?);", first, middle, last, house, birth)
