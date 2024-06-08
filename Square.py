import pygame
from Piece import Piece
class Square:
    def __init__(self, side_length, color, x, y, row, column):
        self.side_length = side_length
        self.color = color
        self.x1 = x
        self.y1 = y
        self.x2 = x + side_length
        self.y2 = y + side_length
        self.piece = None
        self.ROW, self.COLUMN = row, column


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x1, self.y1, self.x2, self.y2))
        if(self.piece != None):
            self.piece.draw(screen)

    def getCoordinates(self):
        return [self.x1, self.y1, self.x2, self.y2]

    def initiatePiece(self, color, player):
        self.piece = Piece(color, (self.x1+(self.side_length // 2)), (self.y1+(self.side_length // 2)), player)

    def updatePiece(self, selected=False, king=False):
        if(self.piece != None):
            self.piece.selected = selected
            self.piece.king = king

    def getPiece(self):
        if(self.piece != None):
            return self.piece
        else:
            return None

    def __repr__(self):
        return f"Square at row {self.ROW} and column {self.COLUMN} with piece {self.piece}"
    def __str__(self):
        return {'side': self.side_length, 'color': self.color, 'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 'y2': self.y2, 'piece': self.piece}