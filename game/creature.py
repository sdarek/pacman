import pygame
from utils.constants import GRID_SIZE

class Creature(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def move(self, direction):
        if direction == "UP":
            self.rect.y -= self.speed
        elif direction == "DOWN":
            self.rect.y += self.speed
        elif direction == "LEFT":
            self.rect.x -= self.speed
        elif direction == "RIGHT":
            self.rect.x += self.speed

    def update(self):
        pass
