import pygame
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog

from helpers import Button
from helpers import LoadImage
from sorting import Sort

import constants as c

def main():
    pygame.init()
    screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('PUNKTU KĀRTOTĀJS (Pixel Sorter)')
    running = True
    clock = pygame.time.Clock()

    # Initialize buttons
    upload_button = Button((c.WIDTH / 2, 50,), "assets/upload.png", None, 150)
    download_button = None

    # For scroll feature
    scroll_offset = 0

    # Initialize image, pixels, and sorter as None
    image = None
    pixels = None
    image_surface = None
    sorter = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle window resize event
            if event.type == pygame.VIDEORESIZE:  
                c.WIDTH, c.HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT), pygame.RESIZABLE)
                upload_button = Button((c.WIDTH / 2, 50 + scroll_offset,), "assets/upload.png", None, 150)
                if download_button:
                    download_button = Button((c.WIDTH / 2, image.height + 150 + scroll_offset), "assets/download.png", None, 150)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if upload_button.check_for_input(pygame.mouse.get_pos()):
                    # Open file dialog when button is clicked
                    root = tk.Tk()
                    root.withdraw()
                    filepath = filedialog.askopenfilename()
                    if filepath:
                        image = LoadImage(filepath)
                        pixels = np.array(image)
                        image_surface = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

                        # Initialize the sorter generator
                        sorter = Sort(pixels)  
            
            if event.type == pygame.MOUSEWHEEL:
                scroll_offset += event.y * c.scroll_speed
                if scroll_offset > 0:
                    scroll_offset = 0
                if image is not None:
                    max_scroll = max(0, (image.height + 200) - c.HEIGHT)
                else:
                    max_scroll = 0
                if abs(scroll_offset) > max_scroll:
                    scroll_offset = -max_scroll

                upload_button = Button((c.WIDTH / 2, 50 + scroll_offset,), "assets/upload.png", None, 150)
                if download_button:
                    download_button = Button((c.WIDTH / 2, image.height + 150 + scroll_offset), "assets/download.png", None, 150)


        # drawing
        screen.fill((255, 255, 255))

        if image_surface:
            screen.blit(image_surface, (c.WIDTH / 2 - image.width // 2, 100 + scroll_offset))
            
            if sorter:
                try:
                    sorted_pixels = next(sorter)
                    image_surface = pygame.image.fromstring(sorted_pixels.tobytes(), image.size, image.mode)
                except StopIteration:
                    download_button = Button((c.WIDTH / 2, image.height + 150 + scroll_offset), "assets/download.png", None, 150)
                    sorter = None

        for button in [upload_button, download_button]:
            if button is not None:
                button.update(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
