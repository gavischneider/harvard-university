#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // store the users name in a variable called name
    string name = get_string("Please enter your name\n");
    printf("hello, %s\n", name);
}