import pygame

pygame.init()

screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption('Lunar Lander')

screen.fill((0, 0, 0,))

clock = pygame.time.Clock()

exited = False
while not exited:
    pygame.display.update()
    clock.tick(30)

