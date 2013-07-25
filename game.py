import pygame
from pygame.locals import *

import ship

pygame.init()

screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Lunar Lander')

bg = pygame.Surface((screen.get_width(), screen.get_height())).convert()
bg.fill((0, 0, 0,))
screen.blit(bg, (0, 0))

shipSprite = ship.Ship((screen.get_height() / 2, screen.get_width() / 2))
screen.blit(shipSprite.image, shipSprite.rect)

pygame.display.update()

clock = pygame.time.Clock()

exited = False
while not exited:
    # what's changed from one frame to another
    #delta = []
    screen.blit(bg, (0, 0))

    shipSprite.update()
    screen.blit(shipSprite.image, shipSprite.rect)

    pygame.display.update()
    clock.tick(30)


    for event in pygame.event.get():
        if event.type == QUIT:
            exited = True
        elif event.type == KEYDOWN and event.key in (K_ESCAPE, K_q):
            exited = True

pygame.quit()
