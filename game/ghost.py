import pygame
import random
from utils.constants import *
from game.creature import Creature

class Ghost(Creature):
    def __init__(self, col, row, game):
        super().__init__("assets/images_cropped/ghost.png", col, row, game)

    def update(self):
        # Tutaj dodaj logikę aktualizacji położenia Duszka na planszy
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)