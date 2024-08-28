from PIL import Image
import numpy as np
import pygame

# When you use yield in a function, it turns that function into a generator

def Sort(pixels):
    row_index = 0
    sorted_rows = []

    while row_index < len(pixels):
        # Sort by brightness
        row = pixels[row_index]
        brightness = np.sum(row, axis=1)
        sorted_indices = np.argsort(brightness)
        sorted_row = row[sorted_indices]
        sorted_rows.append(sorted_row)

        new_img = np.array(sorted_rows + list(pixels[row_index + 1:]))
        yield new_img 

        row_index += 1
