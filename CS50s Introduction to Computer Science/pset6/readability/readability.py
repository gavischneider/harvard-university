from cs50 import get_string

text = get_string('Text:\n')
letters = 0
words = 0
sentences = 0
i = 0

# Go over all the letters in text, enumerate gives us access to the index
for index, letter in enumerate(text):
    # Check if its an uppercase or lowercase letter
    if letter.isalpha():
        letters += 1
    elif letter == ' ' and text[index + 1] != " ":
        words += 1
    elif letter == "." or letter == "!" or letter == "?":
        sentences += 1
words += 1

# index = 0.0588 * L - 0.296 * S - 15.8
index = 0.0588 * (100 * letters / words) - 0.296 * (100 * sentences / words) - 15.8

# Print grade
if index < 1:
    print("Before Grade 1")
elif index >= 16:
     print("Grade 16+");
else:
    print(f"Grade {round(index)}")
