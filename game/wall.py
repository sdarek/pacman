# dot.py
import pygame
from utils.constants import *


class Wall(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(DARKBLUE)
        self.rect = self.image.get_rect()
        self.rect.x = col * GRID_SIZE
        self.rect.y = row * GRID_SIZE
