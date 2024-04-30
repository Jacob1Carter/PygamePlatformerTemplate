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


class Bar:
    def __init__(self, owner, tag, current, maximum, colour_active, colour_inactive, left, top, reverse=False):
        self.owner = owner
        self.tag = tag
        self.width = 100
        self.height = 10
        self.thickness = 3
        self.current = current
        self.maximum = maximum
        self.colour_active = colour_active
        self.colour_inactive = colour_inactive
        self.left = left
        self.top = top
        self.right = self.left + self.width
        self. bottom = self.top + self.height
        self.reverse = reverse

    def display(self, win):
        pygame.draw.rect(
            win,
            self.colour_inactive if self.reverse else self.colour_active,
            (self.left, self.top, self.width, self.height)
        )
        pygame.draw.rect(
            win,
            self.colour_active if self.reverse else self.colour_inactive,
            (
                self.right - int(self.width * (1 - self.current / self.maximum)) if self.reverse else self.left,
                self.top,
                self.width * (0 if self.current == 0 and not self.reverse else (1 - self.current / self.maximum)),
                self.height
            )
        )
#   /ui.py
