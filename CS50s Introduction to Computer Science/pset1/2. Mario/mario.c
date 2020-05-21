#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int maxSize = 8;
    int size = 0;

    // Ask the user to input a pyramid size, and continue to do so until it's valid
    do
    {
        size = get_int("Please enter a number between 1 and 8: \n");
    }
    while (size < 1 || size > 8);

    int row = 1;
    for (int i = 0; i < size; i++)
    {
        // First print out the spaces on the row
        for (int j = 0; j < size - row; j++)
        {
            printf(" ");
        }
        // Then print out the hash marks for the left pyramid
        for (int k = 0; k < row; k++)
        {
            printf("#");
        }
        // Then print the two spaces
        for (int l = 0; l < 2; l++)
        {
            printf(" ");
        }
        // Lastly print out the hash marks for the right pyramid
        for (int m = 0; m < row; m++)
        {
            printf("#");
        }
        row++;
        printf("\n");
    }
}