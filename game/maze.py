# maze.py
import pygame
from utils.constants import WHITE

class Maze(pygame.sprite.Sprite):
    def __init__(self, file_path):
        super().__init__()
        self.image = pygame.Surface((800, 600))
        self.rect = self.image.get_rect()

        # Wczytywanie labiryntu z pliku
        self.maze_data = self.load_maze_from_file(file_path)
        self.create_maze()

    def load_maze_from_file(self, file_path):
        with open(file_path, 'r') as file:
            maze = [[int(cell) for cell in line.strip().split()] for line in file]
        return maze

    def create_maze(self):
        cell_size = 30
        for row in range(len(self.maze_data)):
            for col in range(len(self.maze_data[row])):
                if self.maze_data[row][col] == 1:
                    pygame.draw.rect(self.image, WHITE, (col * cell_size, row * cell_size, cell_size, cell_size))
