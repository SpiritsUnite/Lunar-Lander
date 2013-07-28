import pygame
from pygame.locals import *

import math

import loader

class Ship(pygame.sprite.Sprite):
    def __init__(self, game, origin, bound):
        super(Ship, self).__init__()

        self.image = pygame.Surface((80, 40)).convert_alpha()
        self.image.fill((255, 0, 0))
        self.image = loader.load_image("lander.png")
        self.image = pygame.transform.smoothscale(
                self.image,
                (self.image.get_width()/5, self.image.get_height()/5)
        ).convert_alpha()

        self.game = game
        self.x, self.y = (0, 0)
        self.origin = origin
        self.bound = bound

        self.rot = 0
        self.vx = 0
        self.vy = 0

        self.mass = 10000
        self.fuel = 6000

        self.landed = False

    def set_pos(self, pos):
        self.x, self.y = map(float, pos)

    def get_pos(self):
        return (self.x, self.y - self.get_rect().height/2)
    
    def thrust(self, v):
        self.vx += math.sin(math.radians(self.rot)) * v
        self.vy += math.cos(math.radians(self.rot)) * v

    def update(self):
        # apply forces to velocity

        # apply gravity
        self.vy += -self.get_mass() * 0.00001

        # check keys
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            if self.fuel > 0:
                self.thrust(.5)
                self.fuel -= 10
        if keys[K_RIGHT]:
            self.rot += 5
        if keys[K_LEFT]:
            self.rot -= 5

        self.rot %= 360

        # apply drag
        self.vx *= 0.99
        self.vy *= 0.99

        if abs(self.vx) < .01:
            self.vx = 0
        if abs(self.vy) < .01:
            self.vy = 0

        # move rect
        self.x += self.vx
        self.y += self.vy
        # did we hit the ground?
        if self.y - self.get_rect().height/2 < 0:
            # is it a landing?
            if not self.landed:
                # check for successful landing
                if self.vx**2 + self.vy**2 < 4 and (self.rot + 20) % 360 < 40:
                    print "YAYAYYAY"
                    self.rot = 0
                else:
                    print "CRASHED!!"

            # reverse movements
            self.y = self.get_rect().height/2
            self.x -= self.vx
            self.vy = 0
            self.vx = 0
            self.landed = True
        else:
            self.landed = False


        # sides?
        self.x %= self.bound[0]
        

        #print self.x, self.y
        #print self.rot

    def get_surface(self):
        return pygame.transform.rotate(self.image, -self.rot)

    def get_rect(self):
        rect = self.get_surface().get_rect()
        rect.center = (self.origin[0] + self.x, self.origin[1] - self.y)
        #print rect.center

        return rect

    def get_mass(self):
        return self.mass + self.fuel * 1.443

