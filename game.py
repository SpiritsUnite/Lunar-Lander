import pygame
from pygame.locals import *

import ship

class Game:
    def __init__(self, screen):
        # background
        self.bg = pygame.Surface((screen.get_width(), screen.get_height()))
        self.bg = self.bg.convert()
        self.bg.fill((0, 0, 0,))

        self.screen = screen

        # create lander
        self.lander = ship.Ship(self, (screen.get_width()/2, screen.get_height() - 20))

    def update(self, keys):
        self.screen.blit(self.bg, (0, 0))

        self.lander.update(keys)
        
        self.screen.blit(self.lander.get_surface(),\
                self.lander.get_rect((0, screen.get_height())))


if __name__ == "__main__":
    # initialise pygame
    pygame.init()

    # create screen
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Lunar Lander')

    clock = pygame.time.Clock() 

    game = Game(screen)

    exited = False
    while not exited:
        keys = pygame.key.get_pressed()

        game.update(keys)
        pygame.display.update()
        clock.tick(30)


        for event in pygame.event.get():
            if event.type == QUIT:
                exited = True
            elif event.type == KEYDOWN and event.key in (K_ESCAPE, K_q):
                exited = True

pygame.quit()
