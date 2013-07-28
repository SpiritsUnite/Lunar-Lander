import pygame
from pygame.locals import *

import ship
import loader
import status

import random

class Game:
    def __init__(self, screen):
        self.screen = screen

        # background
        self.bg = pygame.Surface((screen.get_width(), screen.get_height()))
        self.bg = self.bg.convert()
        self.bg.fill((0, 0, 0,))

        # terrain
        minh, h, maxh = 30, 100.0, 170
        ter = pygame.Surface((screen.get_width(), maxh + 30)).convert_alpha()
        ter.fill((0, 255, 0))
        terArr = pygame.surfarray.pixels_alpha(ter)
        self.ter = []
        for i in xrange(screen.get_width()):
            nh = h + random.randint(max(-2, minh - h), min(2, maxh - h))
            try:
                ph = maxh - self.ter[-1]
            except IndexError:
                ph = h
            for j in xrange(0, int(h)):
                terArr[i][j] = 0
                if nh <= j < h:
                    terArr[i][j] = (j - nh + 1) * 255 / (h - nh + 1)
                if ph <= j < h:
                    terArr[i][j] = (j - ph + 1) * 255 / (h - ph + 1)
            self.ter.append(maxh - int(h))
            h = nh
        print self.ter
        terArr = None
        self.bg.blit(ter, (0, screen.get_height() - maxh - 30))

        self.screen.blit(self.bg, (0, 0))

        # create lander
        self.lander = ship.Ship(
                self,
                (0, screen.get_height()),
                (screen.get_width(), screen.get_height()),
        )
        self.lander.set_pos((screen.get_width() / 2, screen.get_height() - 40))

        # statuses
        self.statuses = pygame.sprite.RenderUpdates()
        self.statuses.add(status.FuelStatus((0, 0), self.lander, "Ubuntu", 20))
        self.statuses.add(status.VelStatus((0, 20), self.lander, "Ubuntu", 20))
        self.statuses.add(status.PosStatus((0, 40), self.lander, "Ubuntu", 20))
        self.statuses.add(status.AltStatus((0, 60), self.lander, "Ubuntu", 20))
        pygame.display.update()

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
