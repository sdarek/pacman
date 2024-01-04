import pygame
from utils.constants import GRID_SIZE


class Pacman(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.image = pygame.image.load("assets/images_cropped/braun.png")
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = col * GRID_SIZE
        self.rect.y = row * GRID_SIZE
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.speed = 2

    def update(self, grid, walls, dots):
        # Sprawdzenie czy moze sie przemiescic w nowym kierunku
        if self.next_direction != (0, 0):
            dx = self.next_direction[0] * self.speed
            dy = self.next_direction[1] * self.speed
            self.rect.x = self.rect.x + dx
            self.rect.y = self.rect.y + dy
            if pygame.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = self.rect.x - dx
                self.rect.y = self.rect.y - dy
            else:
                self.direction = self.next_direction
                self.next_direction = (0, 0)

        # Oblicz nowe współrzędne Pacmana
        if self.direction != (0, 0):
            dx = self.direction[0] * self.speed
            dy = self.direction[1] * self.speed

            self.rect.x = self.rect.x + dx
            self.rect.y = self.rect.y + dy

            if pygame.sprite.spritecollide(self, walls, dokill=False):
                self.rect.x = self.rect.x - dx
                self.rect.y = self.rect.y - dy

        pacman_collisions = pygame.sprite.spritecollide(self, dots, dokill=True)

    def draw(self, surface):
        # Narysuj obrazek Pacmana na ekranie
        surface.blit(self.image, self.rect)

    def turn(self, direction):
        self.next_direction = direction
