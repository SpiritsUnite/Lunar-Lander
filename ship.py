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
    
    def thrust(self, v):
        self.vx += math.sin(math.radians(self.rot)) * v
        self.vy += math.cos(math.radians(self.rot)) * v

    def update(self, keys):
        # apply forces to velocity

        # apply gravity
        self.vy += -.1

        # check keys
        if keys[K_UP]:
            self.thrust(.5)
        elif keys[K_RIGHT]:
            self.rot += 5
        elif keys[K_LEFT]:
            self.rot -= 5

        self.rot %= 360

        # apply drag
        self.vx *= 0.99
        self.vy *= 0.99

        if abs(self.vx) < .09:
            self.vx = 0
        if abs(self.vy) < .09:
            self.vy = 0


        # move rect
        self.x += self.vx
        self.y += self.vy

        # did we hit the ground?
        if self.y - self.image.get_height() / 2 < 0:
            self.y = self.image.get_height() / 2
            self.vy = 0

        # sides?
        

        #print self.x, self.y
        print self.rot

    def get_surface(self):
        return pygame.transform.rotate(self.image, -self.rot)

    def get_rect(self, origin):
        rect = self.get_surface().get_rect()
        rect.center = (origin[0] + self.x, origin[1] - self.y)
        #print rect.center

        return rect

