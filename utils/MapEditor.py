import pygame
from constants import *
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, KEYDOWN
import sys


class MapEditor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Map Editor")
        self.clock = pygame.time.Clock()

        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.mouse_down = False
        self.draw_mode = 1  # 1 - rysowanie ścian, 2 - kasowanie ścian, 3 - rysowanie kropek
        self.draw_ghost_mode = None  # None - brak rysowania duszków/Pacmana, 4 - rysowanie duszków, 5 - rysowanie Pacmana

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                self.mouse_down = True
                self.handle_mouse_click(event.pos)
            elif event.type == MOUSEMOTION and self.mouse_down:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_s:
                    self.save_maze("saved_maze.csv")
                elif event.key == pygame.K_l:
                    self.load_maze("saved_maze.csv")
                elif event.key == pygame.K_c:
                    self.clear_maze()
                elif event.key == pygame.K_1:
                    self.draw_mode = 1  # Rysowanie ścian
                    self.draw_ghost_mode = None  # Wyłączenie rysowania duszków/Pacmana
                elif event.key == pygame.K_2:
                    self.draw_mode = 2  # Kasowanie ścian
                    self.draw_ghost_mode = None  # Wyłączenie rysowania duszków/Pacmana
                elif event.key == pygame.K_3:
                    self.draw_mode = 3  # Rysowanie kropek
                    self.draw_ghost_mode = None  # Wyłączenie rysowania duszków/Pacmana
                elif event.key == pygame.K_4:
                    self.draw_mode = None  # Wyłączenie rysowania ścian/kropek
                    self.draw_ghost_mode = 4  # Rysowanie duszków
                elif event.key == pygame.K_5:
                    self.draw_mode = None  # Wyłączenie rysowania ścian/kropek
                    self.draw_ghost_mode = 5  # Rysowanie Pacmana

    def handle_mouse_click(self, pos):
        col = pos[0] // GRID_SIZE
        row = pos[1] // GRID_SIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            if self.draw_mode == 1:
                self.grid[row][col] = 1  # Rysowanie ścian
            elif self.draw_mode == 2:
                self.grid[row][col] = 0  # Kasowanie ścian
            elif self.draw_mode == 3:
                self.grid[row][col] = 2  # Rysowanie kropek
            elif self.draw_ghost_mode == 4:
                self.grid[row][col] = 3  # Rysowanie duszków
            elif self.draw_ghost_mode == 5:
                self.grid[row][col] = 4  # Rysowanie Pacmana

    def draw(self):
        self.screen.fill(BLACK)  # Czarny tło

        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] == 1:
                    pygame.draw.rect(self.screen, WHITE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                elif self.grid[row][col] == 2:
                    dot_image = pygame.image.load("assets/images_cropped/dot.png")
                    dot_image = pygame.transform.scale(dot_image, (GRID_SIZE // 2, GRID_SIZE // 2))
                    self.screen.blit(dot_image, (col * GRID_SIZE + GRID_SIZE // 4, row * GRID_SIZE + GRID_SIZE // 4))
                elif self.grid[row][col] == 3:
                    ghost_image = pygame.image.load("assets/images_cropped/ghost.png")
                    ghost_image = pygame.transform.scale(ghost_image, (GRID_SIZE, GRID_SIZE))
                    self.screen.blit(ghost_image, (col * GRID_SIZE, row * GRID_SIZE))
                elif self.grid[row][col] == 4:
                    pacman_image = pygame.image.load("assets/images_cropped/braun.png")
                    pacman_image = pygame.transform.scale(pacman_image, (GRID_SIZE, GRID_SIZE))
                    self.screen.blit(pacman_image, (col * GRID_SIZE, row * GRID_SIZE))
                else:
                    pygame.draw.rect(self.screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    def save_maze(self, filename):
        with open(filename, 'w') as file:
            for row in self.grid:
                line = ','.join(map(str, row[:COLS]))
                file.write(line + '\n')

    def load_maze(self, filename):
        maze = []
        with open(filename, 'r') as file:
            for line in file:
                row = [int(cell) for cell in line.strip().split(',')][:COLS]
                maze.append(row)
        self.grid = maze

    def clear_maze(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

if __name__ == "__main__":
    editor = MapEditor()
    editor.run()
