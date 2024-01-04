# helpers.py
import pygame

def load_image(file_path):
    try:
        image = pygame.image.load(file_path)
        return image
    except pygame.error as e:
        print(f"Error loading image: {e}")
        return None
