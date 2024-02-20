# game.py
import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN, K_BACKSPACE
import os
import json
from utils.constants import GRID_SIZE, GAME_SIZE, BLUE, WHITE
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
        self.pacman_icon = pygame.image.load("assets/images_cropped/pac.png")
        self.pacman_icon = pygame.transform.scale(self.pacman_icon, (GRID_SIZE, GRID_SIZE))

        self.start_time = pygame.time.get_ticks()
        self.high_scores = []
        self.elapsed_seconds = 0
        self.paused = False
        self.pause_start_time = 0

        self.load_high_scores()

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
                elif event.key == pygame.K_p:
                    self.toggle_pause()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_start_time = pygame.time.get_ticks()
        else:
            if self.pause_start_time > 0:
                pause_duration = pygame.time.get_ticks() - self.pause_start_time
                self.start_time += pause_duration
                self.pause_start_time = 0

    def update(self):
        if not self.paused:
            current_time = pygame.time.get_ticks()
            elapsed_seconds = (current_time - self.start_time) / 1000.
            self.elapsed_seconds = elapsed_seconds
            self.pacman.update()
            self.ghosts.update()

            if self.check_game_over_condition():
                print("aaaa")
                self.show_game_over_screen()

    def check_game_over_condition(self):
        return self.lives <= 0

    def load_high_scores(self):
        if os.path.exists("high_scores.json"):
            with open("high_scores.json", "r") as file:
                self.high_scores = json.load(file)

    def save_high_scores(self):
        with open("high_scores.json", "w") as file:
            json.dump(self.high_scores, file)

    def update_high_scores(self, player_name):
        score_entry = {"name": player_name, "score": self.score, "time": self.elapsed_seconds}
        self.high_scores.append(score_entry)
        self.high_scores = sorted(self.high_scores, key=lambda x: x["score"], reverse=True)[:5]
        self.save_high_scores()

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.elapsed_seconds = 0
        self.start_time = pygame.time.get_ticks()
        self.pacman.reset_position()
        self.paused = False
        for ghost in self.ghosts:
            ghost.reset_position()

    def draw_timer(self):
        time_text = self.font.render(f"Time: {self.elapsed_seconds:.1f}s", True, WHITE)
        time_rect = time_text.get_rect(topleft=(GAME_SIZE[0] - 160, 170))
        self.screen.blit(time_text, time_rect)

    def draw_high_scores(self):
        font = pygame.font.Font(None, 36)
        text = font.render("High Scores", True, WHITE)
        self.screen.blit(text, (GAME_SIZE[0] // 2 - text.get_width() // 2, 200))

        for idx, entry in enumerate(self.high_scores, start=1):
            score_text = f"{idx}. {entry['name']} - Score: {entry['score']} - Time: {entry['time']:.1f}s"
            text = font.render(score_text, True, WHITE)
            self.screen.blit(text, (GAME_SIZE[0] // 2 - text.get_width() // 2, 250 + idx * 40))

    def draw(self):
        self.screen.fill(BLUE)
        self.walls.draw(self.screen)
        self.dots.draw(self.screen)
        self.ghosts.draw(self.screen)
        self.pacman.draw(self.screen)
        for gate in self.gates:
            gate.draw()

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(GAME_SIZE[0] - 100, 50))
        self.screen.blit(score_text, score_rect)

        for i in range(self.lives):
            life_rect = self.pacman_icon.get_rect(topleft=(GAME_SIZE[0] - 150 + i * 40, 100))
            self.screen.blit(self.pacman_icon, life_rect)

        self.draw_timer()
        if self.paused:
            self.draw_pause_screen()

    def draw_pause_screen(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Paused", True, WHITE)
        text_rect = text.get_rect(center=(GAME_SIZE[0] // 2, GAME_SIZE[1] // 2))
        self.screen.blit(text, text_rect)

    def show_game_over_screen(self):
        self.draw()
        self.draw_high_scores()
        self.draw_name_input()
        pygame.display.flip()
        self.get_player_name()
        self.save_high_scores()

    def draw_name_input(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Koniec obrad - Imie:", True, WHITE)
        text_rect = text.get_rect(center=(GAME_SIZE[0] // 2, GAME_SIZE[1] // 2 + 100))
        self.screen.blit(text, text_rect)

    def get_player_name(self):
        input_box = pygame.Rect(GAME_SIZE[0] // 2 - 100, GAME_SIZE[1] // 2 + 150, 200, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_active = True

        while input_active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.update_high_scores(text)
                        self.reset_game()
                        input_active = False
                    elif event.key == K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)
            pygame.display.flip()  # Dodaj odświeżenie ekranu

            clock.tick(30)

        return text

# game.py - koniec
