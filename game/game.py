import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT
from utils.constants import *

from game.pacman import Pacman
from game.ghost import Ghost
from game.dot import Dot
from game.wall import Wall
from game.gate import Gate


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Game(metaclass=SingletonMeta):
    def __init__(self, maze):
        pygame.init()
        self.screen = pygame.display.set_mode(GAME_SIZE)
        pygame.display.set_caption("PacBraun")
        self.clock = pygame.time.Clock()

        self.grid = maze
        self.pacman = None
        self.walls = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.dots = pygame.sprite.Group()
        self.gates = pygame.sprite.Group()

        self.score = 0
        self.lives = 3
        self.font = pygame.font.Font(None, 36)
        self.pacman_icon = pygame.image.load("assets/images_cropped/braun.png")
        self.pacman_icon = pygame.transform.scale(self.pacman_icon, (GRID_SIZE, GRID_SIZE))

        self.start_time = pygame.time.get_ticks()


        # Inicjalizacja obiektów Pacmana, Duszków i Kropki
        for row_idx, row in enumerate(maze):
            for col_idx, cell_value in enumerate(row):
                if cell_value == 4:
                    self.pacman = Pacman(row_idx, col_idx, self)
                elif cell_value == 3:
                    self.ghosts.add(Ghost(col_idx, row_idx, self))
                elif cell_value == 2:
                    self.dots.add(Dot(col_idx, row_idx))
                elif cell_value == 1:
                    self.walls.add(Wall(row_idx, col_idx))
                elif cell_value == 5:
                    self.dots.add(Dot(col_idx, row_idx, True))
                elif cell_value == 6:
                    self.gates.add(Gate(row_idx, col_idx, self))

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(100)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.pacman.turn((0, -1))
                elif event.key == K_DOWN:
                    self.pacman.turn((0, 1))
                elif event.key == K_LEFT:
                    self.pacman.turn((-1, 0))
                elif event.key == K_RIGHT:
                    self.pacman.turn((1, 0))

    def update(self):
        self.pacman.update()
        self.ghosts.update()

    def draw(self):
        self.screen.fill(BLUE)
        self.walls.draw(self.screen)
        self.dots.draw(self.screen)
        self.ghosts.draw(self.screen)
        self.pacman.draw(self.screen)
        for gate in self.gates:
            gate.draw()

        # Rysuj licznik punktów po prawej stronie
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(GAME_SIZE[0] - 100, 50))
        self.screen.blit(score_text, score_rect)

        # Rysuj licznik żyć pod licznikiem punktów
        for i in range(self.lives):
            life_rect = self.pacman_icon.get_rect(topleft=(GAME_SIZE[0] - 150 + i * 40, 100))
            self.screen.blit(self.pacman_icon, life_rect)

        self.draw_timer()

    def draw_timer(self):
        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - self.start_time) / 1000.
        time_text = self.font.render(f"Time: {elapsed_seconds:.1f}s", True, WHITE)
        time_rect = time_text.get_rect(topleft=(GAME_SIZE[0] - 160, 170))
        self.screen.blit(time_text, time_rect)



