import pygame


# setup pygame
BOARD_SIZE = [8, 10, 12]
SCREEN_SIZE = (800, 800)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill('blue')
    pygame.display.flip()
    clock.tick(60)

pygame.quit()