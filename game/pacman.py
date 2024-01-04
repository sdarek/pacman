import pygame
from utils.constants import *


class Pacman:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.direction = (0, 0)  # Kierunek ruchu (dx, dy)

    def move(self, dx, dy, maze):
        new_row = self.row + dy
        new_col = self.col + dx
        if self.is_valid_move(new_row, new_col, maze):
            self.row = new_row
            self.col = new_col

    def is_valid_move(self, new_row, new_col, maze):
        return 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] != 1

    def update(self, maze):
        self.move(self.direction[0], self.direction[1], maze)

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.col * GRID_SIZE + GRID_SIZE // 2, self.row * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2)