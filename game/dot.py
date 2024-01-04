# dot.py
import pygame
from utils.constants import *

class Dot(pygame.sprite.Sprite):
    def __init__(self, col, row):
        super().__init__()

        self.image = pygame.image.load("assets/images_cropped/dot.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE // 2, GRID_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.x = col * GRID_SIZE + GRID_SIZE // 4
        self.rect.y = row * GRID_SIZE + GRID_SIZE // 4
