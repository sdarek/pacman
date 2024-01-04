import pygame
import random
from utils.constants import *

class Ghost(pygame.sprite.Sprite):
    def __init__(self, col, row):
        super().__init__()

        self.image = pygame.image.load("assets/images_cropped/ghost.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = col * GRID_SIZE
        self.rect.y = row * GRID_SIZE

    def update(self, grid):
        # Tutaj dodaj logikę aktualizacji położenia Duszka na planszy
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)