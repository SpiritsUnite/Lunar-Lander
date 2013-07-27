import pygame
from pygame.locals import *

import math

class Ship(pygame.sprite.Sprite):
    def __init__(self, game, pos = (0, 0)):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((20, 40)).convert_alpha()
        self.image.fill((255, 0, 0))

        self.x, self.y = map(float, pos)

        self.rot = 0
        self.vx = 0
        self.vy = 0

        self.mass = 10000
        self.fuel = 6000

        self.landed = False

    def set_pos(self, pos):
        self.x, self.y = map(float, pos)
    
    def thrust(self, v):
        self.vx += math.sin(math.radians(self.rot)) * v
        self.vy += math.cos(math.radians(self.rot)) * v

    def update(self, keys):
        # apply forces to velocity

        # apply gravity
        self.vy += -self.get_mass() * 0.00001

        # check keys
        if keys[K_UP]:
            if self.fuel > 0:
                self.thrust(.5)
                self.fuel -= 10
        if keys[K_RIGHT]:
            self.rot += 7
        if keys[K_LEFT]:
            self.rot -= 7

        self.rot %= 360

        # apply drag
        self.vx *= 0.99
        self.vy *= 0.99

        if abs(self.vx) < .1:
            self.vx = 0
        if abs(self.vy) < .1:
            self.vy = 0


        # move rect
        self.x += self.vx
        self.y += self.vy

        # did we hit the ground?
        if self.y - self.image.get_height() / 2 < 0:
            # is it a landing?
            if not self.landed:
                # check for successful landing
                if self.vx**2 + self.vy**2 < 2 and (self.rot + 20) % 360 < 40:
                    print "YAYAYYAY"
                    self.rot = 0
                else:
                    print "CRASHED!!"

            self.y = self.image.get_height() / 2
            self.vy = 0
            self.vx = 0
            self.landed = True
        else:
            self.landed = False


        # sides?
        

        #print self.x, self.y
        #print self.rot

    def get_surface(self):
        return pygame.transform.rotate(self.image, -self.rot)

    def get_rect(self, origin):
        rect = self.get_surface().get_rect()
        rect.center = (origin[0] + self.x, origin[1] - self.y)
        #print rect.center

        return rect

    def get_mass(self):
        return self.mass + self.fuel * 1.443

