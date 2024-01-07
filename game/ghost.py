import pygame
import random
from utils.constants import *
from game.creature import Creature


class ChaseState:
    def update(self, ghost, pacman):
        pass


class FleeState:
    def update(self, ghost, pacman):
        pass


class RandomState:
    def update(self, ghost, game):
        available_directions = ghost.can_turn()
        new_direction = random.choice(available_directions)
        ghost.next_direction = new_direction
        ghost.move()


class Ghost(Creature):
    def __init__(self, col, row, game):
        super().__init__("assets/images_cropped/ghost.png", col, row, game)

        self.chase_state = ChaseState()
        self.flee_state = FleeState()
        self.random_state = RandomState()
        self.state = self.random_state
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.target = (0, 0)
        self.speed = 1

    def update(self):
        self.target = self.game.pacman.getPosition()
        self.collision = self.wall_collision(self.direction)
        self.state.update(self, self.game)

    def switch_to_chase(self):
        self.state = self.chase_state

    def switch_to_flee(self):
        self.state = self.flee_state

    def switch_to_random(self):
        self.state = self.random_state

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def can_turn(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        directions.remove((-self.direction[0], -self.direction[1]))

        available_directions = []
        for direction in directions:
            if not self.wall_collision(direction):
                available_directions.append(direction)

        if not available_directions:
            available_directions.append((-self.direction[0], -self.direction[1]))

        return available_directions
