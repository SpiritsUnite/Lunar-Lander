import pygame
from pygame.locals import *

class Ship(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.velocity = [0, 0]

    def update(self):
        # apply forces to velocity

        # apply gravity
        self.velocity[1] += 1


        # move rect
        self.rect.move_ip(self.velocity[0], self.velocity[1])


