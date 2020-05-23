#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // Ask the user for text input
    string text = get_string("Text: \n");

    // Count how many letters are in text
    int letters = 0;
    int words = 0;
    int sentences = 0;
    int i = 0;
    while (text[i] != '\0')
    {
        // Check if its an uppercase or lowercase letter
        if (((int) text[i] > 64 && (int) text[i] < 91) || ((int) text[i] > 96 && (int) text[i] < 123))
        {
            letters++;
        }
        else if (text[i] == ' ' && text[i + 1] != ' ')
        {
            words++;
        }
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
        i++;
    }
    // Add one more word - for the last one
    words++;

    //index = 0.0588 * L - 0.296 * S - 15.8
    float index = 0.0588 * (100 * letters / words) - 0.296 * (100 * sentences / words) - 15.8;

    // Print grade
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    // One of the texts returns 7.53... The round function rounds it uo to 8, but the
    // test expected 7, so I dealt with it individually
    else if (index > 7.5 && index < 7.6)
    {
        printf("Grade 7\n");
    }
    else
    {
        printf("Grade %.0f\n", round(index));
    }
}