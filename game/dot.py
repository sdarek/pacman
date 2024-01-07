# dot.py
import pygame
from utils.constants import *

class Dot(pygame.sprite.Sprite):
    def __init__(self, col, row, big=False):
        super().__init__()

        original_image = pygame.image.load("assets/images_cropped/dot.png").convert_alpha()

        if big:
            self.image = pygame.transform.scale(original_image, (GRID_SIZE, GRID_SIZE))
            self.rect = self.image.get_rect(topleft=(col * GRID_SIZE, row * GRID_SIZE))
        else:
            self.image = pygame.transform.scale(original_image, (GRID_SIZE // 2, GRID_SIZE // 2))
            self.rect = self.image.get_rect(topleft=(col * GRID_SIZE + GRID_SIZE // 4, row * GRID_SIZE + GRID_SIZE // 4))

        self.big = big


    def getBig(self):
        return self.big
