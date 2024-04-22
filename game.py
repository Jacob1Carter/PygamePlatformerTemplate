#   game.py
import pygame
from const import COLOURS
from ui import Reticule


class GameClass:
    class DisplayClass:
        def __init__(self):
            self.win = pygame.display.set_mode((900, 500))
            self.display_ui = True

            self.reticule = Reticule()

        def refresh(self, mousex, mousey):
            self.win.fill(COLOURS.black)

            self.refresh_game_view()

            if self.display_ui:
                self.refresh_ui(mousex, mousey, self.reticule)

            pygame.display.update()

        def refresh_game_view(self):
            pass

        def refresh_ui(self, mousex, mousey, reticule):
            #   Reticule
            pygame.draw.line(
                self.win,
                COLOURS.white,
                (mousex - reticule.width / 2 - reticule.gap / 2, mousey - reticule.height / 2 - reticule.gap / 2),
                (mousex - reticule.gap / 2, mousey - reticule.gap / 2),
                reticule.thickness
            )

    class Scene:
        def __init__(self):
            active_entities = []

    def __init__(self):
        self.mouse_visible = False
        self.fps = 120
        self.running = True
        self.clock = pygame.time.Clock()
        self.active_scene = self.Scene()

    display = DisplayClass()

#   /game.py
