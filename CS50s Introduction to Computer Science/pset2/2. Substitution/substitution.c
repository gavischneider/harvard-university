#include <stdio.h>
#include <cs50.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // check if argv[1] is empty
    if (argv[1] == NULL)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    char includedLetters[26];

    // Check key length
    int lowerIndex = 0;
    int upperIndex = 0;
    int in = 0;
    int i = 0;
    int length = 0;
    while (argv[1][i] != '\0')
    {
        // Check if it's an uppercase letter
        if (((int)argv[1][i] > 64 && (int)argv[1][i] < 91))
        {
            length++;
            // Check if we already marked down this letter, if not add it
            int j = 0;
            while (includedLetters[j] != '\0')
            {
                if ((int)includedLetters[j] == argv[1][i])
                {
                    printf("Key must contain 26 DIFFERENT characters.\n");
                    return 1;
                }
                j++;
            }
            char let = argv[1][i];
            includedLetters[in] = let;
            in++;
        }
        // Check if its a lowercase letter
        else if (((int)argv[1][i] > 96 && (int)argv[1][i] < 123))
        {
            length++;
            // Check if we already marked down this letter, if not add it
            int j = 0;
            while (includedLetters[j] != '\0')
            {
                if ((int)includedLetters[j] == argv[1][i])
                {
                    printf("Key must contain 26 DIFFERENT characters.\n");
                    return 1;
                }
                j++;
            }
            char let = argv[1][i];
            includedLetters[in] = let;
            in++;
        }
        else
        {
            printf("Key must contain 26 alphabetic characters.\n");
            return 1;
        }
        i++;
    }
    if (length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // If we've gotten to this point, the cipher input is legit
    string plaintext = get_string("plaintext: ");

    string lowercaseAlphabet = "abcdefghijklmnopqrstuvwxyz";
    string uppercaseAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    printf("ciphertext: ");
    // Now start ciphering

    // Find the letters index in the includedLetters array
    for (int a = 0, ind = 0; plaintext[ind] != '\0'; a++)
    {
        // First check if its a letter, if its not, print it out as is
        if (((int)plaintext[a] > 64 && (int)plaintext[a] < 91) || ((int)plaintext[a] > 96 && (int)plaintext[a] < 123))
        {
            // Go over all the letters in the alphabet
            for (int d = 0; d < 26; d++)
            {
                if (lowercaseAlphabet[d] == plaintext[ind] || uppercaseAlphabet[d] == plaintext[ind])
                {
                    //printf("MADE IT HERE\n");
                    char let = includedLetters[d];

                    // Check which case to print in
                    if (((int)plaintext[a] > 64 && (int)plaintext[a] < 91))
                    {
                        // Uppercase
                        char result = toupper(let);
                        printf("%c", result);
                        break;
                    }
                    else
                    {
                        // Lowercase
                        char result = tolower(let);
                        printf("%c", result);
                        break;
                    }
                }
            }
        }
        // Print as is
        else
        {
            printf("%c", plaintext[ind]);
        }
        ind++;
    }
    printf("\n");
    return 0;
}
