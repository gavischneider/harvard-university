#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    bool startWrite = false;
    bool open = false;

    // Check for invalid usage
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open the file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("File does not exist\n");
        return 1;
    }

    unsigned char buffer[512];
    int fileCount = 0;

    // Open a new JPEG file to write into
    char fileName[8];
    FILE *jpeg = fopen(fileName, "w");

    // Start going through the memory card
    while (fread(&buffer, 512, 1, file) != 0)
    {
        // Check if it's the first JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0 && fileCount == 0)
        {

            sprintf(fileName, "%03i.jpg", fileCount);
            jpeg = fopen(fileName, "w");
            fwrite(buffer, 512, 1, jpeg);
            fileCount++;
        }

        // If it's not the first
        else if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            fclose(jpeg);
            sprintf(fileName, "%03i.jpg", fileCount);
            jpeg = fopen(fileName, "w");
            fwrite(buffer, 512, 1, jpeg);
            fileCount++;
        }

        else if (fileCount > 0)
        {
            fwrite(buffer, 1, 512, jpeg);
        }
    }
    return 0;
}
