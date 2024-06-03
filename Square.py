import pygame

class Square:
    def __init__(self, side, color, x, y):
        self.side = side
        self.color = color
        self.x1 = x
        self.y1 = y
        self.x2 = x + side
        self.y2 = y + side
        self.piece = None

    def area(self):
        return self.side ** 2

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x1, self.y1, self.x2, self.y2))

    def getCoordinates(self):
        return [self.x1, self.y1, self.x2, self.y2]

    def getPiece(self):
        if(self.piece != None):
            return self.piece
        else:
            return None

    def setPiece(self, piece):

    def __str__(self):
        return f"Square with side {self.side}"