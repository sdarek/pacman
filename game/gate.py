# dot.py
import pygame
from utils.constants import *


class Gate(pygame.sprite.Sprite):
    def __init__(self, row, col, game):
        super().__init__()

        self.line_start = (col * GRID_SIZE, row * GRID_SIZE + GRID_SIZE // 2)
        self.line_end = ((col + 1) * GRID_SIZE, row * GRID_SIZE + GRID_SIZE // 2)
        self.line_thickness = 2
        self.game = game

    def draw(self):
        pygame.draw.line(self.game.screen, WALL_COLOR, self.line_start, self.line_end, self.line_thickness)


    def check_collision(self, rect):
        line_rect = pygame.Rect(self.line_start, (self.line_end[0] - self.line_start[0], self.line_thickness))
        return rect.colliderect(line_rect)