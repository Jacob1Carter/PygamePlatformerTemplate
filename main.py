#   main.py
import pygame

from game import GameClass


def main():
    game = GameClass()

    #   run game
    while game.running:
        pygame.mouse.set_visible(game.mouse_visible)
        game.clock.tick(game.fps)

        keys_down = []

        #   handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                keys_down.append(event.key)

        #   set variables
        keys_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        mousex, mousey = pygame.mouse.get_pos()

        #   Game loop

        for entity in game.active_scene.active_entities:
            entity.update(keys_pressed, keys_down, mouse_pressed, mousex, mousey)

        #   refresh display and loop for next frame
        game.display.refresh(mousex, mousey)


if __name__ == "__main__":
    main()

#   /main.py
