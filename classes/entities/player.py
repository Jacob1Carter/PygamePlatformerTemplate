# player.py
import pygame
import math

from classes.ui import Bar
from classes.const import COLOURS
from scripts.tools import calculate_angle, exponential_decay, normalizer
from classes.shared import Entity
from classes.entities.structure import Foreground


class Player(Entity):
    def __init__(self, game):
        super().__init__(game)

        self.transform = self.Transform(100, 400, 50, 100)

        self.state = "fall"

        self.max_health = 1000
        self.health = self.max_health

        self.speed = 600/self.game.fps
        self.gravity = 120/self.game.fps
        self.jump_speed = 600/self.game.fps
        self.jump_time = 0.3*self.game.fps
        self.jump_done = False
        self.fall_done = False
        self.active_jump_time = 0
        self.active_fall_time = 0
        self.terminal_fall_time = 0.9*self.game.fps

        self.colour = COLOURS.blue

        self.gun = self.Gun(self.game, self)

        self.ui.append(Bar(self, "ammo", self.health, self.max_health, COLOURS.black, COLOURS.red, 10, 10, True))

    def check_state(self):
        self.jump_done = False
        self.fall_done = False
        for entity in self.game.active_scene.active_entities:
            if isinstance(entity, Foreground):
                if self.is_overlapping_bottom(entity):
                    self.transform.y = entity.transform.bottom + self.transform.height // 2
                    self.state = "fall"
                elif self.is_overlapping_left(entity):
                    self.transform.x = entity.transform.left - self.transform.width // 2
                    self.state = "wall-right"
                elif self.is_overlapping_right(entity):
                    self.transform.x = entity.transform.right + self.transform.width // 2
                    self.state = "wall-left"
                elif self.is_above(entity):
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
                
                if self.is_overlapping_top(entity):
                    self.transform.y = entity.transform.top - self.transform.height // 2
                    self.state = "idle"
                

    def update(self, keys_pressed, keys_down, mouse_pressed, mousex, mousey):
        self.check_state()

        if keys_pressed[pygame.K_SPACE]:
            if self.state == "idle":
                self.state = "jump"
                self.active_jump_time = 0

        if keys_pressed[pygame.K_a]:
            if self.state != "wall-left":
                self.transform.x -= self.speed
        if keys_pressed[pygame.K_d]:
            if self.state != "wall-right":
                self.transform.x += self.speed

        if self.state == "jump":
            decay_factor = 0.995
            jump_speed = exponential_decay(self.jump_speed, decay_factor, self.active_jump_time)
            self.transform.y -= jump_speed
        elif self.state == "fall":
            self.transform.y += self.game.active_scene.gravity*self.gravity * normalizer(
                self.active_fall_time, self.terminal_fall_time
            )

        self.gun.update(keys_down, mouse_pressed, mousex, mousey)


        if self.transform.y > self.game.display.resolution[1]:
            self.health = 0

    def display(self, win):
        super().display(win)

        pygame.draw.rect(
            win,
            self.colour,
            (self.transform.left, self.transform.top, self.transform.width, self.transform.height)
        )

        self.gun.display(win)

    class Gun(Entity):
        def __init__(self, game, player):
            super().__init__(game)
            self.transform = self.Transform(player.transform.left, player.transform.top, 3, 100)
            self.player = player

            self.colour = COLOURS.black

            self.bullets = []

            self.max_cooldown = 0.1*self.game.fps
            self.cooldown = 0

            self.max_ammo = 30
            self.ammo = self.max_ammo

            self.reload_speed = 1*self.game.fps
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
            self.transform.x = self.player.transform.x
            self.transform.y = self.player.transform.y
            self.transform.angle = calculate_angle(self.transform.x, self.transform.y, mousex, mousey)

            if pygame.K_r in keys_down:
                if self.ammo < self.max_ammo:
                    self.ammo = 0
                    self.state = "reload"
                    self.reload_time = self.reload_speed

            if self.cooldown > 0:
                self.cooldown -= 1
            else:
                if mouse_pressed[0]:
                    if self.state == "active":
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
            self.bullets.append(self.Bullet(self, self.game))
            self.cooldown = self.max_cooldown
            self.ammo -= 1

        def display(self, win):
            super().display(win)

            pygame.draw.line(
                win,
                self.colour,
                (self.transform.x, self.transform.y),
                (
                    self.transform.x + self.transform.height * math.cos(math.radians(self.transform.angle)),
                    self.transform.y + self.transform.height * math.sin(math.radians(self.transform.angle))
                ),
                self.transform.width
            )

            for bullet in self.bullets:
                bullet.display(win)

        class Bullet(Entity):
            def __init__(self, gun, game):
                super().__init__(game)
                self.gun = gun
                self.transform.x = gun.transform.x + gun.transform.height * math.cos(math.radians(gun.transform.angle))
                self.transform.y = gun.transform.y + gun.transform.height * math.sin(math.radians(gun.transform.angle))
                self.transform.width = 3
                self.transform.height = 3
                self.speed = 3400/self.game.fps
                self.transform.angle = gun.transform.angle
                self.active = True
                self.colour = COLOURS.black

            def update(self):
                self.transform.x += self.speed * math.cos(math.radians(self.transform.angle))
                self.transform.y += self.speed * math.sin(math.radians(self.transform.angle))

                if self.transform.x < 0 or self.transform.x > self.game.display.resolution[0] or \
                        self.transform.y < 0 or self.transform.y > self.game.display.resolution[1]:
                    self.active = False

                for entity in self.game.active_scene.active_entities:
                    if isinstance(entity, Foreground):
                        if self.is_within(entity):
                            self.active = False

            def display(self, win):
                pygame.draw.circle(
                    win,
                    self.colour,
                    (self.transform.x, self.transform.y),
                    self.transform.width
                )


# /player.py
