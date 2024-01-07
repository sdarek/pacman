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
        self.collision = False
        self.next_collision = False

    def move(self):
        if self.next_direction != (0, 0):
            if not self.next_collision:
                self.direction = self.next_direction
                self.next_direction = (0, 0)

        if self.direction != (0, 0):
            if not self.collision:
                dx = self.direction[0] * self.speed
                dy = self.direction[1] * self.speed
                self.rect.x = self.rect.x + dx
                self.rect.y = self.rect.y + dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def turn(self, direction):
        self.next_direction = direction

    def wall_collision(self, direction):
        dx = direction[0] * self.speed
        dy = direction[1] * self.speed
        copy_rect = self.rect.copy()
        copy_rect.x += dx
        copy_rect.y += dy
        temp_sprite = pygame.sprite.Sprite()
        temp_sprite.rect = copy_rect
        if pygame.sprite.spritecollide(temp_sprite, self.game.walls, dokill=False):
            return True
        return False

    def update(self):
        pass
