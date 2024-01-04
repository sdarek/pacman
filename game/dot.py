# dot.py
import pygame
from utils.constants import WHITE
from utils.helpers import load_image

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("assets/images_cropped/dot.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
