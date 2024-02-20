#pacman.py
import pygame
from utils.constants import GRID_SIZE
from game.creature import Creature


class Pacman(Creature):
    def __init__(self, row, col, game):
        super().__init__("assets/images_cropped/pac.png", col, row, game)
        self.speed = 2

    def update(self):
        self.collision = self.wall_collision(self.direction)
        self.next_collision = self.wall_collision(self.next_direction)
        self.move()
        #print(f"{self.direction} {self.next_direction}")

        # zjedzenie gasnicy
        pacbraun_dot_collision = pygame.sprite.spritecollide(self, self.game.dots, dokill=True)
        if pacbraun_dot_collision:
            if pacbraun_dot_collision[0].getBig():
                self.game.score += 20
                for ghost in self.game.ghosts:
                    ghost.switch_to_flee()
            else:
                self.game.score += 1

        # Sprawdź kolizję Pacbrauna z duszkami
        pacman_ghost_collisions = pygame.sprite.spritecollide(self, self.game.ghosts, dokill=False)
        if pacman_ghost_collisions:
            if pacman_ghost_collisions[0].getCanBeEaten():
                self.game.score += 10
                pacman_ghost_collisions[0].reset_position()
            else:
                self.game.lives -= 1
                self.reset_position()
        for gate in self.game.gates:
            if gate.check_collision(self.rect):
                self.rect.x -= self.direction[0] * self.speed
                self.rect.y -= self.direction[1] * self.speed



    def reset_position(self):
        self.direction = (0, 0)
        self.rect.x = self.start_position_x
        self.rect.y = self.start_position_y

    def getPosition(self):
        return self.rect.x, self.rect.y
