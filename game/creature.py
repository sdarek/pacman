from re import S
import pygame
from utils.constants import GRID_SIZE

class Creature(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, game):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * GRID_SIZE
        self.rect.y = y * GRID_SIZE
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.game = game
        self.speed = 1

    def move(self):
        if self.next_direction != (0, 0):
            dx = self.next_direction[0] * self.speed
            dy = self.next_direction[1] * self.speed
            self.rect.x = self.rect.x + dx
            self.rect.y = self.rect.y + dy
            if pygame.sprite.spritecollide(self, self.game.walls, dokill=False):
                self.rect.x = self.rect.x - dx
                self.rect.y = self.rect.y - dy
            else:
                self.direction = self.next_direction
                self.next_direction = (0, 0)
        
        if self.direction != (0, 0):
            dx = self.direction[0] * self.speed
            dy = self.direction[1] * self.speed

            self.rect.x = self.rect.x + dx
            self.rect.y = self.rect.y + dy
            if pygame.sprite.spritecollide(self, self.game.walls, dokill=False):
                self.rect.x = self.rect.x - dx
                self.rect.y = self.rect.y - dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def turn(self, direction):
        self.next_direction = direction

    def update(self):
        pass
