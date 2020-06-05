import cs50
import csv
from sys import argv, exit

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

# Open DNA sequence
with open(argv[2], 'r') as file:
    dnaSeq = file.read()

# Extract info from CSV file and put it into a dictionary
with open(argv[1]) as file:
    csvFile = csv.DictReader(file)

    # Sequences hold all the column titles (name, STRs)
    sequences = csvFile.fieldnames
    numOfSeq = len(sequences)

# Define a set that will hold the occurrences of each STR in dnaSeq
results = {}

# For each STR, see how many times it appears consecutively in dnaSeq
for i in range(1, numOfSeq):
    results[sequences[i]] = 0
    seqlen = len(sequences[i])

    # Iterate over all the letters looking for DNA matches
    for j in range(len(dnaSeq)):
        tmpcounter = 0
        while sequences[i] == dnaSeq[j:(j + seqlen)]:
            tmpcounter += 1
            j += seqlen
        if results[sequences[i]] < tmpcounter:
            results[sequences[i]] = tmpcounter

# Now we to to compare the results to each row in our csvFile
with open(argv[1], "r") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        for key, value in row.items():
            if value.isnumeric():
                strMatch = str(results[key])
                if value == strMatch:
                    match = True
                else:
                    match = False
                    break
        if match:
            print(row['name'])
            exit(0)

print("No match")