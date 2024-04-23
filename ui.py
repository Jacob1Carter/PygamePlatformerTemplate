#   ui.py
import pygame

from const import COLOURS


class Reticule:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.thickness = 1
        self.dot = 0
        self.gap = 0
        self.colour = COLOURS.white

    def display(self, mousex, mousey, win):
        pygame.draw.line(
            win,
            self.colour,
            (mousex - self.width / 2 - self.gap / 2, mousey),
            (mousex - self.gap / 2, mousey),
            self.thickness
        )  # left line
        pygame.draw.line(
            win,
            self.colour,
            (mousex + self.gap / 2, mousey),
            (mousex + self.width / 2 + self.gap / 2, mousey),
            self.thickness
        )  # right line
        pygame.draw.line(
            win,
            self.colour,
            (mousex, mousey - self.gap / 2),
            (mousex, mousey - self.height / 2 - self.gap / 2),
            self.thickness
        )  # top line
        pygame.draw.line(
            win,
            self.colour,
            (mousex, mousey + self.gap / 2),
            (mousex, mousey + self.height / 2 + self.gap / 2),
            self.thickness
        )  # bottom line
        pygame.draw.circle(
            win,
            self.colour,
            (mousex, mousey),
            self.dot
        )  # dot

#   /ui.py
