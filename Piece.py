import pygame


class Piece:
    def __init__(self, color, x, y, player):
        self.color = color
        self.x = x
        self.y = y
        self.king = False
        self.player = player
        self.selected = False

    def draw(self, screen):
        if self.selected:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 45)
        else:
            pygame.draw.circle(screen, (90, 90, 90), (self.x, self.y), 45)
        pygame.draw.circle(screen, self.color, (self.x, self.y), 40)


    def __str__(self):
        return f"Piece at {self.x}, {self.y} with color {self.color} and player {self.player}"