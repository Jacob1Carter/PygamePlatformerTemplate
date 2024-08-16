# gui.py
import pygame

from classes.const import COLOURS
from classes.shared import Entity


class Title(Entity):
    def __init__(self, game, text):
        super().__init__(game)
        self.transform.x = game.display.resolution[0] // 2
        self.transform.y = int(game.display.resolution[1] * 0.15)
        #0.425 (ignore this)
        self.text = text
    
    def display(self, win):
        super().display(win)

        font = pygame.font.Font(None, 72)
        text = font.render(self.text, True, COLOURS.white)
        win.blit(
            text,
            (self.transform.x - text.get_width() // 2, self.transform.y - text.get_height() // 2)
        )


class Button(Entity):
    def __init__(self, game, toggle=False):
        super().__init__(game)
        self.transform.width = 400
        self.transform.height = 80
        self.transform.x = game.display.resolution[0] // 2
        self.transform.y = game.display.resolution[1] // 2
        self.transform.left = self.transform.x - self.transform.width // 2
        self.transform.top = self.transform.y - self.transform.height // 2

        self.text = ""

        self.colour_off = COLOURS.blue
        self.colour_on = COLOURS.green
        self.colour_hover = COLOURS.olive

        self.state = "off"

        self.toggle = toggle

        self.max_click_cool_down = 0.4 * self.game.fps
        self.click_cool_down = 0
        self.actiontime = 0.2 * self.game.fps
        self.last_tick = self.max_click_cool_down
    
    def display(self, win):
        super().display(win)

        if self.state == "on":
            colour = self.colour_on
        elif self.state == "hover":
            colour = self.colour_hover
        else:
            colour = self.colour_off

        pygame.draw.rect(
            win,
            colour,
            (self.transform.left, self.transform.top, self.transform.width, self.transform.height)
        )

        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, COLOURS.white)
        win.blit(
            text,
            (self.transform.x - text.get_width() // 2, self.transform.y - text.get_height() // 2)
        )
    
    def is_pressed(self, mousex, mousey, mouse_pressed):
        return self.transform.left <= mousex <= self.transform.left + self.transform.width and self.transform.top <= mousey <= self.transform.top + self.transform.height and mouse_pressed[0] and self.click_cool_down <= 0
    
    def is_hovered(self, mousex, mousey):
        return self.transform.left <= mousex <= self.transform.left + self.transform.width and self.transform.top <= mousey <= self.transform.top + self.transform.height

    def update(self, keys_pressed, keys_down, mouse_pressed, mousex, mousey):
        if self.is_hovered(mousex, mousey):
            if self.state != "on":
                self.state = "hover"
        else:
            if self.state != "on":
                self.state = "off"

        if self.is_pressed(mousex, mousey, mouse_pressed):
            if self.state != "on":
                self.state = "on"
            else:
                self.state = "off"
            self.click_cool_down = self.max_click_cool_down

        self.last_tick = self.click_cool_down

        if self.click_cool_down > 0:
            self.click_cool_down -= 1

            if self.last_tick > self.actiontime >= self.click_cool_down:
                self.action()
        else:
            if self.state == "on" and not self.toggle:
                self.state = "off"
            self.click_cool_down = 0
    
    def action(self):
        pass


class ResumeButton(Button):
    def __init__(self, game):
        super().__init__(game)
        self.text = "Resume"
    
    def action(self):
        if self.state == "on":
            self.game.mouse_visible = not self.game.mouse_visible
            if type(self.game.active_scene) != self.game.PauseScene:
                self.game.paused_scene = self.game.active_scene
                self.game.active_scene = self.game.PauseScene(self.game)
            else:
                self.game.active_scene = self.game.paused_scene
                self.game.paused_scene = None


# /gui.py
