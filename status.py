import pygame
from pygame.locals import *

import loader

class Status(pygame.sprite.Sprite):
    def __init__(self, font, size, topleft, lander):
        super(Status, self).__init__()
        
        try:
            self.font = loader.load_font(font, size)
        except IOError:
            self.font = loader.load_sys_font(font, size)

        self.lander = lander
        self.update()
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft

    def update(self):
        raise NotImplementedError

class FuelStatus(Status):
    def update(self):
        text = "Fuel: %d" % (self.lander.fuel)
        self.image = self.font.render(text, True, (255,255,255))

class VelStatus(Status):
    def update(self):
        text = "Velocity: (%lf, %lf, %lf)" % (self.lander.vx, self.lander.vy,
                (self.lander.vx**2 + self.lander.vy**2)**.5)
        self.image = self.font.render(text, True, (255,255,255))

class PosStatus(Status):
    def update(self):
        text = "Position: (%lf, %lf)" % (self.lander.x, self.lander.y)
        self.image = self.font.render(text, True, (255,255,255))

class AltStatus(Status):
    def update(self):
        text = "Altitude: %lf" % (self.lander.y)
        self.image = self.font.render(text, True, (255,255,255))

