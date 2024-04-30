#   entities.py
import pygame

from ui import Bar
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

        self.max_health = 1000
        self.health = self.max_health

        self.speed = 600/game.fps
        self.gravity = 120/game.fps
        self.jump_speed = 600/game.fps
        self.jump_time = 0.3*game.fps
        self.jump_done = False
        self.fall_done = False
        self.active_jump_time = 0
        self.active_fall_time = 0
        self.terminal_fall_time = 0.9*game.fps

        self.ui = []

        self.gun = self.Gun(self)

        self.ui.append(Bar(self, "ammo", self.health, self.max_health, COLOURS.black, COLOURS.red, 10, 10, True))

    def check_state(self):
        self.jump_done = False
        self.fall_done = False
        for entity in self.game.active_scene.active_entities:
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

    def update(self, keys_pressed, keys_down, mouse_pressed, mousex, mousey):
        self.check_state()

        if keys_pressed[pygame.K_SPACE]:
            if self.state == "idle":
                self.state = "jump"
                self.active_jump_time = 0

        if keys_pressed[pygame.K_a]:
            if self.state != "wall-left":
                self.x -= self.speed
        if keys_pressed[pygame.K_d]:
            if self.state != "wall-right":
                self.x += self.speed

        if self.state == "jump":
            decay_factor = 0.995
            jump_speed = exponential_decay(self.jump_speed, decay_factor, self.active_jump_time)
            self.y -= jump_speed
        elif self.state == "fall":
            self.y += self.game.active_scene.gravity*self.gravity * normalizer(
                self.active_fall_time, self.terminal_fall_time
            )

        self.gun.update(keys_down, mouse_pressed, mousex, mousey)

    def update_ui(self):
        pass

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

            self.max_cooldown = 0.1*player.game.fps
            self.cooldown = 0

            self.max_ammo = 30
            self.ammo = self.max_ammo

            self.reload_speed = 1*player.game.fps
            self.reload_time = 0

            self.state = "active"
            
            player.ui.append(Bar(
                self,
                "ammo",
                self.ammo,
                self.max_ammo,
                COLOURS.black,
                COLOURS.purple,
                10,
                50,
                True
            ))
            player.ui.append(Bar(
                self,
                "reload",
                self.reload_time,
                self.reload_speed,
                COLOURS.black,
                COLOURS.blue,
                10,
                70
            ))

        def update(self, keys_down, mouse_pressed, mousex, mousey):
            self.x = self.player.x
            self.y = self.player.y
            self.angle = calculate_angle(self.x, self.y, mousex, mousey)

            if pygame.K_r in keys_down:
                self.ammo = 0
                self.state = "reload"
                self.reload_time = self.reload_speed

            if self.cooldown > 0:
                self.cooldown -= 1
            else:
                if mouse_pressed[0]:
                    if self.ammo > 0:
                        self.shoot()
                    elif self.reload_time == 0:
                        self.state = "reload"
                        self.reload_time = self.reload_speed
                elif self.cooldown != 0:
                    self.cooldown = 0

            if self.state == "reload":
                if self.reload_time <= 0:
                    self.ammo = self.max_ammo
                    self.reload_time = 0
                    self.state = "active"
                else:
                    self.reload_time -= 1

            for bullet in self.bullets:
                bullet.update()

                if not bullet.active:
                    self.bullets.remove(bullet)

            self.update_ui()

        def update_ui(self):
            for ui in self.player.ui:
                if ui.owner == self:
                    if isinstance(ui, Bar):
                        if ui.tag == "ammo":
                            ui.current = self.ammo
                            ui.maximum = self.max_ammo
                        elif ui.tag == "reload":
                            ui.current = self.reload_time
                            ui.maximum = self.reload_speed

        def shoot(self):
            self.bullets.append(self.Bullet(self))
            self.cooldown = self.max_cooldown
            self.ammo -= 1

        def display(self, win):
            pygame.draw.line(
                win,
                COLOURS.black,
                (self.x, self.y),
                (
                    self.x + self.height * math.cos(math.radians(self.angle)),
                    self.y + self.height * math.sin(math.radians(self.angle))
                ),
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
                self.speed = 3400/self.gun.player.game.fps
                self.angle = gun.angle
                self.active = True

            def update(self):
                self.x += self.speed * math.cos(math.radians(self.angle))
                self.y += self.speed * math.sin(math.radians(self.angle))

                if self.x < 0 or self.x > self.gun.player.game.display.resolution[0] or \
                        self.y < 0 or self.y > self.gun.player.game.display.resolution[1]:
                    self.active = False

                for entity in self.gun.player.game.active_scene.active_entities:
                    if isinstance(entity, Foreground):
                        if entity.left < self.x < entity.right and entity.top < self.y < entity.bottom:
                            self.active = False

            def update_ui(self):
                pass

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
        self.ui = []

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

    def update(self, keys_pressed, keys_down, mouse_pressed, mousex, mousey):
        pass

    def update_ui(self):
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
