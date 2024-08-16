# shared.py
import pygame
import math

from classes.ui import Bar
from classes.const import COLOURS

class Scene:
    def __init__(self):
        self.gravity = 10
        self.active_entities = []

class Entity:
    def __init__(self, game):
        self.transform = self.Transform()
        self.ui = []
        self.game = game

    class Transform:
        def __init__(self, left=0, top=0, width=0, height=0):
            self.left = left
            self.top = top
            self.width = width
            self.height = height
            self.right = self.left + self.width
            self.bottom = self.top + self.height
            self.x = self.left + self.width // 2
            self.y = self.top + self.height // 2
            self.angle = 0

    def update(self, keys_pressed, keys_down, mouse_pressed, mousex, mousey):
        pass

    def update_ui(self):
        pass

    def display(self, win):
        self.transform.left = self.transform.x - self.transform.width // 2
        self.transform.top = self.transform.y - self.transform.height // 2
        self.transform.right = self.transform.left + self.transform.width
        self.transform.bottom = self.transform.top + self.transform.height

        # debug
        pygame.draw.circle(
            win,
            COLOURS.black,
            (self.transform.x, self.transform.y),
            2
        )
        # /debug
    
    def get_closest_point(self, entity): # fix this
        if self.transform.x < entity.transform.x:
            x = entity.transform.left
        elif self.transform.x > entity.transform.x:
            x = entity.transform.right
        else:
            x = self.transform.x

        if self.transform.y < entity.transform.y:
            y = entity.transform.top
        elif self.transform.y > entity.transform.y:
            y = entity.transform.bottom
        else:
            y = self.transform.y

        return x, y

    def get_distance(self, entity, center=True):
        if center:
            return math.sqrt((self.transform.x - entity.transform.x) ** 2 + (self.transform.y - entity.transform.y) ** 2)
        else:
            self.get_closest_point(entity)
            #then get distance
            return 0 # fix this
    
    def get_angle(self, entity, center=True):
        if center:
            return math.degrees(math.atan2(entity.transform.y - self.transform.y, entity.transform.x - self.transform.x))
        else:
            self.get_closest_point(entity)
            #then get angle
            return 0 # fix this
    
    def is_above(self, entity):
        return self.transform.bottom < entity.transform.top
    
    def is_below(self, entity):
        return self.transform.top > entity.transform.bottom
    
    def is_left(self, entity):
        return self.transform.right < entity.transform.left
    
    def is_right(self, entity):
        return self.transform.left > entity.transform.right

    def is_on_top(self, entity):
        return self.transform.bottom == entity.transform.top and entity.transform.left < self.transform.x < entity.transform.right
    
    def is_overlapping_top(self, entity):
        return entity.transform.bottom > self.transform.bottom >= entity.transform.top and not self.is_left(entity) and not self.is_right(entity)
    
    def is_overlapping_bottom(self, entity):
        return entity.transform.top < self.transform.top < entity.transform.bottom and not self.is_left(entity) and not self.is_right(entity)
    
    def is_overlapping_left(self, entity):
        return entity.transform.right > self.transform.right > entity.transform.left and entity.transform.bottom > self.transform.y > entity.transform.top
    
    def is_overlapping_right(self, entity):
        return entity.transform.right > self.transform.left > entity.transform.left and entity.transform.bottom > self.transform.y > entity.transform.top
    
    def is_within(self, entity):
        return entity.transform.left < self.transform.x < entity.transform.right and entity.transform.top < self.transform.y < entity.transform.bottom

# /shared.py
