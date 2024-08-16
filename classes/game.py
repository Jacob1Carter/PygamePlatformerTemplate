# game.py
import pygame
from classes.const import COLOURS
from classes.entities.player import Player
from classes.entities.structure import Foreground
from classes.shared import Scene
from classes.ui import Reticule
from classes.entities.gui import ResumeButton, Title


class GameClass:
    class DisplayClass:
        resolutions = [(1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)]

        def __init__(self, game):
            self.game = game
            self.resolution = self.resolutions[0]
            self.fullscreen = False
            self.win = pygame.display.set_mode(self.resolution)
            self.display_ui = True

            self.reticule = Reticule(game)

        def refresh(self, mousex, mousey):
            self.win.fill(COLOURS.dark_grey)

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

            for entity in self.game.active_scene.active_entities:
                for ui in entity.ui:
                    ui.display(self.win)

    class Scene1(Scene):
        def __init__(self, game):
            super().__init__()
            self.active_entities = [Player(game), Foreground(game=game, resolution=game.display.resolution), Foreground(game=game, top=game.display.resolution[1]-250, left=400, width=250, height=100)]

    class PauseScene(Scene):
        def __init__(self, game):
            super().__init__()
            self.gravity = 0
            self.active_entities = [Title(game, "Paused"), ResumeButton(game), ResumeButton(game)]

            count = sum(1 for obj in self.active_entities if not isinstance(obj, Title))

            button_height = 110
            
            if count > 1:
                centerpoint = int(game.display.resolution[1] * 0.525)
                
                point = int(centerpoint - (button_height * count) // 2)
                
                for obj in self.active_entities:
                    if not isinstance(obj, Title):
                        obj.transform.top = point
                        obj.transform.y = obj.transform.top + obj.transform.height // 2

                        point += button_height

    def __init__(self):
        self.mouse_visible = False
        self.fps = 144
        self.running = True
        self.clock = pygame.time.Clock()
        self.display = self.DisplayClass(self)
        self.active_scene = self.Scene1(self)
        self.paused_scene = None

# /game.py
