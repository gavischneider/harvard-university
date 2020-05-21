#include <stdio.h>
#include <cs50.h>

bool isValid(long);
void checkSum(long);

int main(void)
{
     long cardNumber = get_long("Credit card number: \n");
     bool rightLength = isValid(cardNumber);
     if(!rightLength)
     {
         // Invalid Card
        printf("INVALID\n");
        return 0;
     }

    // Now we will apply check sum
    checkSum(cardNumber);
}



bool isValid(long cardNumber)
{
    // Check card number length
    int count;
    for (count = 0; cardNumber > 0; count++)
    {
        cardNumber /= 10;
    }

    if (count == 15 || count == 16 || count == 13)
    {
        return true;
    }
    return false;
}

void checkSum(long cardNumber)
{
    long cardCopy = cardNumber;
    long cardCopy2 = cardNumber;
    int firstSum = 0;
    int secondSum = 0;

    // Get number length
    int count;
    for (count = 0; cardCopy > 0; count++)
    {
        cardCopy /= 10;
    }

    if(count %2 == 0) // Count is even
    {
        // Now we start the check sum algorithm
        for(int i = count - 1; i >= 0; i--)
        {
            int num = cardNumber % 10;

            // Check if index is odd or even
            if (i %2 != 0) //
            {
                secondSum += num;
            }
            else // Odd - multiply by two
            {
                num *= 2;
                // Check if greater than 10, meaning 2 digits
                if(num > 9)
                {
                    int temp = num % 10;
                    num /= 10;
                    num += temp;
                }
                firstSum += num;
            }
            cardNumber /= 10;
        }
    }
    else // Count is odd
    {
        // Now we start the check sum algorithm
        for(int i = count - 1; i >= 0; i--)
        {
            int num = cardNumber % 10;

            // Check if index is odd or even
            if (i %2 == 0) //
            {
                 secondSum += num;
            }
            else // Odd - multiply by two
            {
                num *= 2;
                // Check if greater than 10, meaning 2 digits
                if(num > 9)
                {
                    int temp = num % 10;
                    num /= 10;
                    num += temp;
                }
                firstSum += num;
            }
            cardNumber /= 10;
        }
    }

    int finalSum = firstSum + secondSum;
    if (finalSum % 10 != 0)
    {
        // Invalid Card
        printf("INVALID\n");
        return;
    }

    // If we got here the card is valid, now we'll check what kind of card it is;


    // Check for Amex
    if (count == 15)
    {
        while (cardCopy2 > 100)
        {
            cardCopy2 /= 10;
        }
        if (cardCopy2 == 34 || cardCopy2 == 37)
        {
            printf("AMEX\n");
            return;
        }
        else
        {
             // Invalid Card
            printf("INVALID\n");
            return;
        }
    }
    // Check for Visa, part 1
    else if (count == 13)
    {
        while (cardCopy2 > 10)
        {
            cardCopy2 /= 10;
        }
        if (cardCopy2 == 4)
        {
            printf("VISA\n");
            return;
        }
        else
        {
             // Invalid Card
            printf("INVALID\n");
            return;
        }
    }
    // Length is 16, check for Visa part 2 and MasterCard
    else
    {
        while (cardCopy2 > 100)
        {
            cardCopy2 /= 10;
        }
        if (cardCopy2 == 51 || cardCopy2 == 52 || cardCopy2 == 53 || cardCopy2 == 54 || cardCopy2 == 55)
        {
            // MasterCard
            printf("MASTERCARD\n");
            return;
        }
        // Check if Visa
        else
        {
            cardCopy2 /= 10;
            if(cardCopy2 == 4)
            {
                printf("VISA\n");
                return;
            }
            else
        {
             // Invalid Card
            printf("INVALID\n");
            return;
        }
        }
    }
}