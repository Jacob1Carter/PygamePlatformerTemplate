#   main.py
import pygame

from game import GameClass
from entities import Player


def main():
    game = GameClass()

    #   run game
    while game.running:
        pygame.mouse.set_visible(game.mouse_visible)
        game.clock.tick(game.fps)

        #   handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        #   set variables
        keys_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        mousex, mousey = pygame.mouse.get_pos()

        #   Game loop

        for entity in game.active_scene.active_entities:
            entity.move(keys_pressed, mouse_pressed, mousex, mousey)

            if isinstance(entity, Player):
                entity.check_state(game.active_scene.active_entities)

        #   refresh display and loop for next frame
        game.display.refresh(mousex, mousey)


if __name__ == "__main__":
    main()

#   /main.py
