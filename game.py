#   game.py
import pygame
from const import COLOURS
from entities import Player, Floor
from ui import Reticule


class GameClass:
    class DisplayClass:
        resolutions = [(1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)]

        def __init__(self, game):
            self.game = game
            self.resolution = self.resolutions[0]
            self.fullscreen = False
            self.win = pygame.display.set_mode(self.resolution)
            self.display_ui = True

            self.reticule = Reticule()

        def refresh(self, mousex, mousey):
            self.win.fill(COLOURS.black)

            self.refresh_game_view()

            if self.display_ui:
                self.refresh_ui(mousex, mousey, self.reticule)

            pygame.display.update()

        def refresh_game_view(self):
            for entity in self.game.active_scene.active_entities:
                entity.display(self.win)

        def refresh_ui(self, mousex, mousey, reticule):
            #   Reticule
            reticule.display(mousex, mousey, self.win)

    class Scene:
        def __init__(self):
            self.active_entities = [Player(), Floor(0, 0, 0, 0)]

    def __init__(self):
        self.mouse_visible = False
        self.fps = 120
        self.running = True
        self.clock = pygame.time.Clock()
        self.active_scene = self.Scene()
        self.display = self.DisplayClass(self)

#   /game.py
