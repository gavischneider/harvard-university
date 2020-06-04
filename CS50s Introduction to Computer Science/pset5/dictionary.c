// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
const unsigned int N = 100;

// Hash table
node *table[N];

unsigned int wordCount = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    unsigned int linkedList = hash(word);

    node *tempNode = table[linkedList];

    // Start traversing list
    while (tempNode != NULL)
    {
        if (strcasecmp(tempNode->word, word) == 0)
        {
            return true;
        }
        tempNode = tempNode->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Jenkins "One at a Time" hash
    int hash, i;
    for (hash = i = 0; i < strlen(word); ++i)
    {
        hash += tolower(word[i]);
        hash += (hash << 10);
        hash ^= (hash >> 6);
    }
    hash += (hash << 3);
    hash ^= (hash >> 11);
    hash += (hash << 15);
    return (hash % N);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open the file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("File does not exist\n");
        return false;
    }
    // Start reading words from file
    char newWord[LENGTH + 1];

    node *n;
    while (fscanf(file, "%s", newWord) != EOF)
    {
        n = malloc(sizeof(node));
        if (n == NULL)
        {
            printf("Malloc error\n");
            unload();
            return 1;
        }
        strcpy(n->word, newWord);
        n->next = NULL;

        // Get hash index
        unsigned int index = hash(newWord);

        // Insert new node into linked list -> table[index]
        if (table[index] == NULL)
        {
            // First node
            table[index] = n;
        }
        else
        {
            // Not first node
            n->next = table[index];
            table[index] = n;
        }
        wordCount++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *temp;
    node *crawler;

    for (int i = 0; i < N; i++) // Run for length of table
    {
        if (table[i] != NULL) // If there's no node, ignore
        {
            crawler = table[i]; // Go to each node and free
            while (crawler != NULL)
            {
                temp = crawler->next;
                free(crawler);
                crawler = temp;
            }
            temp = crawler;
            free(temp);
        }
    }
    return true;
}
