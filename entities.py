#   entities.py
import pygame

from const import COLOURS


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def display(self, win):
        pygame.draw.circle(
            win,
            COLOURS.white,
            (self.x, self.y),
            5
        )


class Floor:
    def __init__(self, left, top, width, height):
        self.colour = COLOURS.white
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def display(self, win):
        pygame.draw.rect(
            win,
            self.colour,
            (self.left, self.top, self.width, self.height)
        )

#   /entities.py
