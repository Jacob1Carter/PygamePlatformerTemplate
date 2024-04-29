#   entities.py
import pygame

from const import COLOURS

import math


def calculate_angle(x, y, a, b):
    dx = a - x
    dy = b - y
    return math.degrees(math.atan2(dy, dx))


def normalizer(lower, higher):
    if lower >= higher:
        return 1
    elif lower <= 0:
        return 0
    else:
        return lower / higher


def exponential_decay(initial_speed, decay_factor, time):
    return initial_speed * (decay_factor ** time)


class Player:
    def __init__(self, game):
        self.game = game

        self.x = 100
        self.y = 400
        self.width = 50
        self.height = 100

        self.left = self.x - self.width // 2
        self.top = self.y - self.height // 2
        self.right = self.left + self.width
        self.bottom = self.top + self.height

        self.state = "fall"

        self.gravity = 1
        self.jump_speed = 5
        self.jump_time = 0.3*game.fps
        self.jump_done = False
        self.fall_done = False
        self.active_jump_time = 0
        self.active_fall_time = 0
        self.terminal_fall_time = 0.9*game.fps

        self.gun = self.Gun(self)

    def check_state(self, entities):
        self.jump_done = False
        self.fall_done = False
        for entity in entities:
            if isinstance(entity, Foreground):
                if self.bottom < entity.top:
                    if self.state == "jump":
                        if self.active_jump_time < self.jump_time:
                            if not self.jump_done:
                                self.active_jump_time += 1
                                self.jump_done = True
                        else:
                            self.state = "fall"
                            self.active_fall_time = 0
                            self.active_jump_time = 0
                    elif self.state == "fall":
                        if self.active_fall_time < self.terminal_fall_time:
                            if not self.fall_done:
                                self.active_fall_time += 1
                        else:
                            self.active_fall_time = self.terminal_fall_time
                    else:
                        self.state = "fall"
                        self.active_fall_time = 0
                        self.active_jump_time = 0
                elif self.bottom >= entity.top:
                    if self.y > entity.top:
                        if self.right > entity.left and self.left < entity.right:
                            if self.x - entity.left > entity.right - self.x:
                                self.x = entity.right + self.width // 2
                                self.state = "wall-left"
                            else:
                                self.x = entity.left - self.width // 2
                                self.state = "wall-right"
                    else:
                        if self.state != "jump":
                            if entity.left < self.x < entity.right:
                                self.y = entity.top - self.height // 2
                                self.state = "idle"

    def move(self, keys_pressed, mouse_pressed, mousex, mousey):
        if keys_pressed[pygame.K_SPACE]:
            if self.state == "idle":
                self.state = "jump"
                self.active_jump_time = 0

        if keys_pressed[pygame.K_a]:
            if self.state != "wall-left":
                self.x -= 5
        if keys_pressed[pygame.K_d]:
            if self.state != "wall-right":
                self.x += 5

        if self.state == "jump":
            decay_factor = 0.995
            jump_speed = exponential_decay(self.jump_speed, decay_factor, self.active_jump_time)
            self.y -= jump_speed
        elif self.state == "fall":
            self.y += self.game.active_scene.gravity*self.gravity * normalizer(self.active_fall_time, self.terminal_fall_time)

        self.gun.move(mouse_pressed, mousex, mousey)

    def display(self, win):
        self.left = self.x - self.width // 2
        self.top = self.y - self.height // 2
        self.right = self.left + self.width
        self.bottom = self.top + self.height

        pygame.draw.rect(
            win,
            COLOURS.indigo,
            (self.left, self.top, self.width, self.height)
        )
        pygame.draw.circle(
            win,
            COLOURS.black,
            (self.x, self.y),
            2
        )

        self.gun.display(win)

    class Gun:
        def __init__(self, player):
            self.player = player
            self.x = player.x
            self.y = player.y
            self.width = 3
            self.height = 100
            self.angle = 0

            self.bullets = []

        def move(self, mouse_pressed, mousex, mousey):
            self.x = self.player.x
            self.y = self.player.y
            self.angle = calculate_angle(self.x, self.y, mousex, mousey)

            if mouse_pressed[0]:
                self.bullets.append(self.Bullet(self))

            for bullet in self.bullets:
                bullet.move()
                if bullet.x < 0 or bullet.x > self.player.game.display.resolution[0] or bullet.y < 0 or bullet.y > self.player.game.display.resolution[1]:
                    self.bullets.remove(bullet)

        def display(self, win):
            pygame.draw.line(
                win,
                COLOURS.black,
                (self.x, self.y),
                (self.x + self.height * math.cos(math.radians(self.angle)), self.y + self.height * math.sin(math.radians(self.angle))),
                self.width
            )
            pygame.draw.circle(
                win,
                COLOURS.black,
                (self.x, self.y),
                2
            )

            for bullet in self.bullets:
                bullet.display(win)

        class Bullet:
            def __init__(self, gun):
                self.gun = gun
                self.x = gun.x + gun.height * math.cos(math.radians(gun.angle))
                self.y = gun.y + gun.height * math.sin(math.radians(gun.angle))
                self.width = 3
                self.height = 3
                self.speed = 10
                self.angle = gun.angle

            def move(self):
                self.x += self.speed * math.cos(math.radians(self.angle))
                self.y += self.speed * math.sin(math.radians(self.angle))

            def display(self, win):
                pygame.draw.circle(
                    win,
                    COLOURS.black,
                    (self.x, self.y),
                    self.width
                )


class Foreground:
    def __init__(self, left=-1, top=-1, width=-1, height=-1, resolution=None):
        self.colour = COLOURS.white

        if width == -1:
            self.width = resolution[0]
        else:
            self.width = width

        if height == -1:
            self.height = 150
        else:
            self.height = height

        if left == -1:
            self.left = 0
        else:
            self.left = left

        if top == -1:
            self.top = resolution[1] - self.height
        else:
            self.top = top

        self.x = self.left + self.width // 2
        self.y = self.top + self.height // 2
        self.right = self.left + self.width
        self.bottom = self.top + self.height

    def move(self, keys_pressed, mouse_pressed, mousex, mousey):
        pass

    def display(self, win):
        self.x = self.left + self.width // 2
        self.y = self.top + self.height // 2
        self.right = self.left + self.width
        self.bottom = self.top + self.height

        pygame.draw.rect(
            win,
            self.colour,
            (self.left, self.top, self.width, self.height)
        )
        pygame.draw.circle(
            win,
            COLOURS.black,
            (self.x, self.y),
            2
        )

#   /entities.py
