import pygame
from Board import Board


# setup pygame
BOARD_SIZE = [8, 10, 12]
SCREEN_SIZE = (800, 800)
pygame.init()
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
FPS = 60

def main():
    running = True
    clock = pygame.time.Clock()
    board = Board(12, 12, 12)
    SCREEN.fill((0, 0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                square = board.find_square_by_pos(pos)
                board.setSelected(square)
                pygame.display.flip()
        board.draw(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
