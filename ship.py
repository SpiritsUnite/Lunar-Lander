import pygame
from pygame.locals import *

import math

import loader

class Ship(pygame.sprite.Sprite):
    def __init__(self, game, origin, bound):
        super(Ship, self).__init__()

        self.image = loader.load_image("lander.png")
        self.image = pygame.transform.smoothscale(
                self.image,
                (self.image.get_width()/5, self.image.get_height()/5)
        ).convert_alpha()

        self.flame = loader.load_image("flame.png")
        self.flame = pygame.transform.smoothscale(
                self.flame,
                (17, 40)
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
        self.fire = False

    def set_pos(self, pos):
        self.x, self.y = map(float, pos)

    def get_pos(self):
        return (self.x, self.y - self.get_rect().height/2)
    
    def thrust(self, v):
        self.vx += math.sin(math.radians(self.rot)) * v
        self.vy += math.cos(math.radians(self.rot)) * v

    def update(self):
        if self.landed:
            return
        # reset flags
        self.fire = False

        # apply forces to velocity

        # apply gravity
        self.vy += -self.get_mass() * 0.00001

        # check keys
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            if self.fuel > 0:
                self.thrust(.5)
                self.fuel -= 10
                self.fire = True
        if keys[K_RIGHT]:
            self.rot = min(self.rot + 5, 90)
        if keys[K_LEFT]:
            self.rot = max(self.rot - 5, -90)

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
        # sides?
        self.x %= self.bound[0]

        rect = self.get_rect()
        # Find the two highest points under the "legs"
        l, r = rect.left, rect.right
        if self.rot > 0:
            r = int(r - self.image.get_height() * math.sin(math.radians(self.rot)))
        elif self.rot < 0:
            l = int(l - self.image.get_height() * math.sin(math.radians(self.rot)))

        ml, mr = 0, 0
        xl, xr = 0, 0
        for i in xrange(l, l + 12):
            if i < 0:
                ml = -1
                xl = -1
                break
            try:
                if self.game.ter[i] > ml:
                    ml = self.game.ter[i]
                    xl = i
            except IndexError:
                ml = -1
                xl = -1
                break

        for i in xrange(r - 12, r):
            try:
                if self.game.ter[i] > mr:
                    mr = self.game.ter[i]
                    xr = i
            except IndexError:
                mr = -1
                xr = -1
                break
        if ml != -1: ml += 30
        if mr != -1: mr += 30

        #ll, lr = pygame.Surface((self.bound[0], 1)), pygame.Surface((self.bound[0], 1))
        #ll.fill((255,0,0))
        #lr.fill((0,0,255))
        #self.game.screen.blit(self.game.bg, (0, 0))
        #self.game.screen.blit(ll, (0, self.origin[1] - ml))
        #self.game.screen.blit(lr, (0, self.origin[1] - mr))
        #pygame.display.update()

        h = self.image.get_height()
        # did we hit the ground?
        #if self.y - rect.height/2 < ml or self.y - rect.height/2 < mr:
        if self.vy < 0 and ((self.rot >= 0 and (self.y - rect.height/2 < mr or
            self.y - rect.height/2 + h * math.sin(math.radians(self.rot)) < ml)) or
            (self.rot < 0 and (self.y - rect.height/2 < ml or
                self.y - rect.height/2 - h * math.sin(math.radians(self.rot)) < mr))):
            # is it a landing?
            if not self.landed:
                ro = math.degrees(math.atan(abs(ml - mr) / float(xr - xl)))
                if mr > ml:
                    ro = -ro;
                # check for successful landing
                if self.vx**2 + self.vy**2 < 5 and abs(self.rot - ro) < 10:
                    self.rot = ro
                    self.landed = ["Good Landing!"]
                else:
                    self.landed = ["Bad Landing!"]
                    if self.vx**2 + self.vy**2 >= 4:
                        self.landed.append("Too fast!")
                    if abs(self.rot - ro) >= 10:
                        self.landed.append("Rotation not good enough!")
                        self.landed.append("Should be no more than 10 degrees of %lf" % ro)

            # reverse movements
            #self.y = self.get_rect().height/2 + max(mr, ml)
            if self.rot >= 0:
                if self.y - rect.height/2 < mr:
                    self.y = mr + rect.height/2
                else:
                    self.y = ml + rect.height/2 - h * math.sin(math.radians(self.rot))
            else:
                if self.y - rect.height/2 < ml:
                    self.y = ml + rect.height/2
                else:
                    self.y = mr + rect.height/2 + h * math.sin(math.radians(self.rot))
            self.x -= self.vx
            self.vy = 0
            self.vx = 0
        else:
            self.landed = False

        #print self.x, self.y
        #print self.rot

    def get_surface(self):
        #dot = pygame.Surface((10, 10))
        #dot.fill((255, 0, 0))
        #dot = pygame.transform.rotate(dot.convert_alpha(), -self.rot)
        surf = pygame.transform.rotate(self.image, -self.rot)
        #surf.blit(dot,
        #        (surf.get_rect().center[0] + 35*math.sin(math.radians(-self.rot)) - 5,
        #         surf.get_rect().center[1] + 35*math.cos(math.radians(-self.rot)) - 5))
        return surf

    def get_rect(self):
        rect = self.get_surface().get_rect()
        rect.center = (self.origin[0] + self.x, self.origin[1] - self.y)
        #print rect.center

        return rect

    def get_fire(self):
        if not self.fire: return None
        fire = pygame.transform.rotate(self.flame, 180-self.rot)
        return fire

    def get_fire_rect(self):
        rect = self.get_fire().get_rect()
        rect.center = (
                self.origin[0] + self.x + 53*math.sin(math.radians(-self.rot)),
                self.origin[1] - self.y + 52*math.cos(math.radians(-self.rot))
        )
        return rect

    def get_mass(self):
        return self.mass + self.fuel * 1.443

