# structure.py
import pygame

from classes.shared import Entity
from classes.const import COLOURS

class Foreground(Entity):
    def __init__(self, game, left=-1, top=-1, width=-1, height=-1, resolution=None):
        super().__init__(game)
        self.colour = COLOURS.white
        self.ui = []

        if width == -1:
            self.transform.width = resolution[0]
        else:
            self.transform.width = width

        if height == -1:
            self.transform.height = 150
        else:
            self.transform.height = height

        if left == -1:
            self.transform.left = 0
        else:
            self.transform.left = left

        if top == -1:
            self.transform.top = resolution[1] - self.transform.height
        else:
            self.transform.top = top

        self.transform.x = self.transform.left + self.transform.width // 2
        self.transform.y = self.transform.top + self.transform.height // 2
        self.transform.right = self.transform.left + self.transform.width
        self.transform.bottom = self.transform.top + self.transform.height
    
    def display(self, win):
        super().display(win)

        pygame.draw.rect(
            win,
            self.colour,
            (self.transform.left, self.transform.top, self.transform.width, self.transform.height)
        )

# /structure.py
