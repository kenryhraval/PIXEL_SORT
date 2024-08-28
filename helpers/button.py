import pygame

class Button:
    def __init__(self, pos, path, text_input=None, width=None):
        # Store the paths for the normal and clicked images
        self.normal_image_path = path
        self.clicked_image_path = self._get_clicked_image_path(path)

        # Load the normal image using Pygame
        self.image = pygame.image.load(self.normal_image_path).convert_alpha()

        # Resize the image if width is provided
        if width is not None:
            # Get the original size
            original_width, original_height = self.image.get_size()
            # Calculate proportional height
            aspect_ratio = original_height / original_width
            new_width = width
            new_height = int(new_width * aspect_ratio)
            # Resize image
            self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = pygame.font.SysFont("Paradox King Script", 30)
        self.base_color, self.hovering_color = (100, 100, 100), (0, 0, 0)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def _get_clicked_image_path(self, path):
        """Generate the clicked image path based on the original path."""
        file_extension = path.split('.')[-1]
        return path.replace(f'.{file_extension}', f'_clicked.{file_extension}')

    def update(self, screen):
        # Update the image based on mouse position
        self.change_color(pygame.mouse.get_pos())
        # Draw the image and text
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        """Check if the button was clicked based on the mouse position."""
        return self.rect.collidepoint(position)

    def change_color(self, position):
        """Change the button image based on mouse hover state."""
        if self.rect.collidepoint(position):
            # Load and resize clicked image
            new_image = pygame.image.load(self.clicked_image_path).convert_alpha()
        else:
            # Load and resize normal image
            new_image = pygame.image.load(self.normal_image_path).convert_alpha()

        # Resize the new image to match the current size
        new_image = pygame.transform.scale(new_image, self.image.get_size())
        self.image = new_image
