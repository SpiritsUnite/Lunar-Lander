import pygame
from pygame.locals import *

import ship
import loader
import status

class Game:
    def __init__(self, screen):
        # background
        self.bg = pygame.Surface((screen.get_width(), screen.get_height()))
        self.bg = self.bg.convert()
        self.bg.fill((0, 0, 0,))

        self.screen = screen

        # create lander
        self.lander = ship.Ship(self, (0, screen.get_height()))
        self.lander.set_pos((screen.get_width() / 2, screen.get_height() - 40))

        # statuses
        self.statuses = pygame.sprite.RenderUpdates()
        self.statuses.add(status.FuelStatus("Ubuntu", 20, (0, 0), self.lander))
        self.statuses.add(status.VelStatus("Ubuntu", 20, (0, 20), self.lander))
        self.statuses.add(status.PosStatus("Ubuntu", 20, (0, 40), self.lander))
        self.statuses.add(status.AltStatus("Ubuntu", 20, (0, 60), self.lander))

    def display(self):
        # Clear previous frame
        rects = [self.screen.blit(self.bg, self.lander.get_rect(),
                self.lander.get_rect())]
        self.statuses.clear(self.screen, self.bg)

        # Update
        self.lander.update()
        self.statuses.update()
        
        rects.append(self.screen.blit(self.lander.get_surface(),
            self.lander.get_rect()))
        rects.extend(self.statuses.draw(screen))

        # display
        pygame.display.update(rects)
        


if __name__ == "__main__":
    # initialise pygame
    pygame.init()

    # create screen
    screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('Lunar Lander')

    clock = pygame.time.Clock() 

    game = Game(screen)

    exited = False
    while not exited:

        game.display()
        clock.tick(30)


        for event in pygame.event.get():
            if event.type == QUIT:
                exited = True
            elif event.type == KEYDOWN and event.key in (K_ESCAPE, K_q):
                exited = True

pygame.quit()
