import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT
from utils.constants import *

from game.pacman import Pacman
from game.ghost import Ghost
from game.dot import Dot


class Game:
    def __init__(self, maze):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Pac-Braun Game")
        self.clock = pygame.time.Clock()

        self.grid = maze
        self.pacman = Pacman(1, 1)
        self.ghosts = [Ghost(len(maze) - 2, len(maze[0]) - 2)]

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(10)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.pacman.direction = (0, -1)
                elif event.key == K_DOWN:
                    self.pacman.direction = (0, 1)
                elif event.key == K_LEFT:
                    self.pacman.direction = (-1, 0)
                elif event.key == K_RIGHT:
                    self.pacman.direction = (1, 0)

    def update(self):
        self.pacman.update(self.grid)
        for ghost in self.ghosts:
            ghost.update(self.grid)

    def draw(self):
        self.screen.fill(BLACK)

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if self.grid[row][col] == 1:
                    pygame.draw.rect(self.screen, WHITE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif self.grid[row][col] == 2:
                    pygame.draw.circle(self.screen, RED,
                                       (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2),
                                       GRID_SIZE // 2)
                elif self.grid[row][col] == 3:
                    pygame.draw.circle(self.screen, BLUE,
                                       (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2),
                                       GRID_SIZE // 2)
                elif self.grid[row][col] == 4:
                    pygame.draw.circle(self.screen, PINK,
                                       (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2),
                                       GRID_SIZE // 2)

        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)
