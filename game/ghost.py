#ghost.py
import pygame
import random
from utils.constants import *
from game.creature import Creature

RANDOM_SPEED = 2
CHASE_SPEED = 3
FLEE_SPEED = 1

class ChaseState:
    def update(self, ghost, pacman):
        pass


class FleeState:
    def update(self, ghost, pacman):
        # Sprawdź, czy minęło 30 sekund od rozpoczęcia ucieczki
        elapsed_time = (pygame.time.get_ticks() - ghost.flee_start_time) / 1000.0
        if elapsed_time >= 10:
            ghost.switch_to_random()

        available_directions = ghost.can_turn()
        new_direction = random.choice(available_directions)
        ghost.next_direction = new_direction
        ghost.move()


class RandomState:
    def update(self, ghost, game):
        available_directions = ghost.can_turn()
        new_direction = random.choice(available_directions)
        ghost.next_direction = new_direction
        ghost.move()


class Ghost(Creature):
    image_paths = ["assets/images_cropped/pacblue.png",
                   "assets/images_cropped/pacorange.png",
                   "assets/images_cropped/pacred.png"]
    used_paths = set()
    def __init__(self, col, row, game):
        unused_paths = list(set(Ghost.image_paths) - set(Ghost.used_paths))
        if not unused_paths:
            Ghost.used_paths.clear()
            unused_paths = Ghost.image_paths
        image_path = random.choice(unused_paths)
        Ghost.used_paths.add(image_path)
        super().__init__(image_path, col, row, game)

        self.chase_state = ChaseState()
        self.flee_state = FleeState()
        self.random_state = RandomState()
        self.state = self.random_state
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.target = (0, 0)
        self.speed = RANDOM_SPEED
        self.can_be_eaten = False
        self.flee_start_time = 0
        self.in_home = True

    def update(self):
        self.target = self.game.pacman.getPosition()
        self.collision = self.wall_collision(self.direction)
        self.state.update(self, self.game)
        if self.in_home:
            for gate in self.game.gates:
                if gate.check_collision(self.rect):
                    if not gate.check_collision(pygame.Rect(self.rect.x + self.direction[0], self.rect.y + self.direction[1], self.rect.width, self.rect.height)):
                        self.in_home = False
                        break
        elif not self.in_home:
            for gate in self.game.gates:
                if gate.check_collision(self.rect):
                    self.rect.x -= self.direction[0] * self.speed
                    self.rect.y -= self.direction[1] * self.speed
                    self.direction = (-self.direction[0], -self.direction[1])
                    break


    def switch_to_chase(self):
        self.can_be_eaten = False
        self.speed = CHASE_SPEED
        self.state = self.chase_state

    def switch_to_flee(self):
        self.flee_start_time = pygame.time.get_ticks()
        self.can_be_eaten = True
        self.speed = FLEE_SPEED
        self.state = self.flee_state

    def getCanBeEaten(self):
        return self.can_be_eaten

    def switch_to_random(self):
        self.can_be_eaten = False
        self.speed = RANDOM_SPEED
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

    def reset_position(self):
        self.rect.x = self.start_position_x
        self.rect.y = self.start_position_y
        self.in_home = True;
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

