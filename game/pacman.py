import pygame
from utils.constants import GRID_SIZE
from game.creature import Creature


class Pacman(Creature):
    def __init__(self, row, col, game):
        super().__init__("assets/images_cropped/braun.png", col, row, game)
        self.start_position_x = col * GRID_SIZE
        self.start_position_y = row * GRID_SIZE
        self.speed = 1

    def update(self):
        self.collision = self.wall_collision(self.direction)
        self.next_collision = self.wall_collision(self.next_direction)
        self.move()
        #print(f"{self.direction} {self.next_direction}")
        # zjedzenie gasnicy
        pacman_collisions = pygame.sprite.spritecollide(self, self.game.dots, dokill=True)
        if pacman_collisions:
            self.game.score += 1

        # Sprawdź kolizję Pacbrauna z duszkami
        pacman_ghost_collisions = pygame.sprite.spritecollide(self.game.pacman, self.game.ghosts, dokill=False)
        if pacman_ghost_collisions:
            self.game.lives -= 1
            self.direction = (0, 0)
            if self.game.lives <= 0:
                print("Game Over")
                pygame.quit()
                exit()
            else:
                self.game.pacman.reset_position()

    def reset_position(self):
        self.rect.x = self.start_position_x
        self.rect.y = self.start_position_y

    def getPosition(self):
        return self.rect.x, self.rect.y
