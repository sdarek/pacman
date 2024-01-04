import pygame
import random
from utils.constants import *

class Ghost:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.direction = (0, 0)

    def move(self, maze):
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        valid_moves = [(dx, dy) for dx, dy in possible_moves if self.is_valid_move(self.row + dy, self.col + dx, maze)]

        if valid_moves:
            self.direction = random.choice(valid_moves)

    def is_valid_move(self, new_row, new_col, maze):
        return 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] != 1

    def update(self, maze):
        self.move(maze)

    def draw(self, screen):
        pygame.draw.circle(screen, PINK, (self.col * GRID_SIZE + GRID_SIZE // 2, self.row * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2)