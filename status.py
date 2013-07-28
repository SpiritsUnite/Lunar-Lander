import pygame
from pygame.locals import *

import loader

class Status(pygame.sprite.Sprite):
    def __init__(self, topleft, lander):
        super(Status, self).__init__()

        self.lander = lander
        self.topleft = topleft

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.topleft

class TextStatus(Status):
    def __init__(self, topleft, lander, font, size):
        super(TextStatus, self).__init__(topleft, lander)

        try:
            self.font = loader.load_font(font, size)
        except IOError:
            self.font = loader.load_sys_font(font, size)

class FuelStatus(TextStatus):
    def update(self):
        text = "Fuel: %d" % (self.lander.fuel)
        self.image = self.font.render(text, True, (255,255,255))

        super(FuelStatus, self).update();

class FuelGuiStatus(Status):
    def update(self):
        pass

class VelStatus(TextStatus):
    def update(self):
        text = "Velocity: (%lf, %lf, %lf)" % (self.lander.vx, self.lander.vy,
                (self.lander.vx**2 + self.lander.vy**2)**.5)
        self.image = self.font.render(text, True, (255,255,255))
        super(VelStatus, self).update();

class PosStatus(TextStatus):
    def update(self):
        text = "Position: (%lf, %lf)" % self.lander.get_pos()
        self.image = self.font.render(text, True, (255,255,255))
        super(PosStatus, self).update()

class AltStatus(TextStatus):
    def update(self):
        text = "Altitude: %lf" % self.lander.get_pos()[1]
        self.image = self.font.render(text, True, (255,255,255))
        super(AltStatus, self).update()


