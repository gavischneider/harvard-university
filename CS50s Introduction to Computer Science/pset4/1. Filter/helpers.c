#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Get the current pixels RGB average
            int avg = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.00);

            // Create new pixel
            RGBTRIPLE newPixel;
            newPixel.rgbtBlue = avg;
            newPixel.rgbtGreen = avg;
            newPixel.rgbtRed = avg;

            // Place newPixel in image
            image[i][j] = newPixel;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Get the original colors
            int originalBlue = image[i][j].rgbtBlue;
            int originalGreen = image[i][j].rgbtGreen;
            int originalRed = image[i][j].rgbtRed;

            // Calculate sepia values
            int sepiaRed = round((.393 * originalRed) + (.769 * originalGreen) + (.189 * originalBlue));
            int sepiaGreen = round((.349 * originalRed) + (.686 * originalGreen) + (.168 * originalBlue));
            int sepiaBlue = round((.272 * originalRed) + (.534 * originalGreen) + (.131 * originalBlue));

            // Cap pixels values at 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            // Create new pixel
            RGBTRIPLE newPixel;
            newPixel.rgbtBlue = sepiaBlue;
            newPixel.rgbtGreen = sepiaGreen;
            newPixel.rgbtRed = sepiaRed;

            // Place newPixel in image
            image[i][j] = newPixel;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        // Reverse array
        int start = 0;
        int end = width - 1;
        while (start < end)
        {
            RGBTRIPLE temp = image[i][start];
            image[i][start] = image[i][end];
            image[i][end] = temp;
            start++;
            end--;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE newImage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // For each pixel, get its box average
            int avgRed = 0;
            int avgGreen = 0;
            int avgBlue = 0;
            float count = 0.00;
            for (int k = (i - 1); k < (i - 1) + 3; k++)
            {
                if (k < 0 || k > height - 1)
                {
                    continue;
                }
                for (int m = (j - 1); m < (j - 1) + 3; m++)
                {
                    if (m < 0 || m > width - 1)
                    {
                        continue;
                    }
                    avgRed += image[k][m].rgbtRed;
                    avgGreen += image[k][m].rgbtGreen;
                    avgBlue += image[k][m].rgbtBlue;
                    count++;
                }
            }

            // Create new pixel
            RGBTRIPLE newPixel;
            newPixel.rgbtBlue = round(avgBlue / count);
            newPixel.rgbtGreen = round(avgGreen / count);
            newPixel.rgbtRed = round(avgRed / count);

            // Place newPixel in image
            newImage[i][j] = newPixel;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = newImage[i][j];
        }
    }
    return;
}
