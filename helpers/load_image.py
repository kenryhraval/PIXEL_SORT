from PIL import Image
import numpy as np

# Load the image using PIL
# Convert the image to a numpy array for pixel manipulation
# Convert the image to a Pygame surface for initial display
def LoadImage(filepath):
    image = Image.open(filepath)
    return image
    