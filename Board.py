import pygame
from Square import Square


class Board:
    def __init__(self, cols, rows):
        self.COLS = cols
        self.ROWS = rows
        self.squares = []
        self.turn = 'player2'
        self.player1_left, self.player2_left = 12, 12 # treba zmenit potom ked sa vyberie difficulty to trocha pomenit
        self.changedSquares = []
        self._selected = None
        self.initiateSquares()
        self.initiatePieces()


    def initiateSquares(self):
        for i in range(self.COLS):
            for j in range(self.ROWS):
                if (i+j) % 2 == 0:
                    new_square = Square(100, (235, 245, 238), i*100, j*100, j, i)
                    self.squares.append(new_square)
                    self.changedSquares.append(new_square)
                else:
                    new_square = Square(100, (139, 120, 109), i*100, j*100, j, i)
                    self.squares.append(new_square)
                    self.changedSquares.append(new_square)

    def initiatePieces(self):
        for i in range(0, 3):
            for j in range(0, self.COLS):
                if self.squares[j*self.COLS+i].color == (139, 120, 109):
                    self.squares[j*self.COLS+i].initiatePiece((235, 245, 238), 'player1')
                    # self.changedSquares.append(self.squares[j*self.COLS+i])

        for i in range(5, 8):
            for j in range(0, self.COLS):
                if self.squares[j*self.COLS+i].color == (235, 245, 238):
                    self.squares[j*self.COLS+i].initiatePiece((139, 120, 109), 'player2')
                    # self.changedSquares.append(self.squares[j*self.COLS+i])

        self.changedSquares = self.squares

    def getSquare(self, x, y):
        for square in self.squares:
            if square.x1 <= x <= square.x2 and square.y1 <= y <= square.y2:
                return square
        return None

    def getPiece(self, x, y):
        square = self.getSquare(x, y)
        if square != None:
            return square.getPiece()
        return None

    def find_square_by_pos(self, pos):
        for square in self.squares:
            if square.x1 <= pos[0] <= square.x2 and square.y1 <= pos[1] <= square.y2:
                return square
        return None

    def get_valid_moves(self, square):
        if square.piece != None:
            if square.piece.player == 'player1':
                return self.get_valid_moves_player1(square)
            else:
                return self.get_valid_moves_player2(square)
        return []

    # def get_valid_moves_player1(self, square):
    #     moves = []
    #     if square.piece.king:
    #         moves += self.get_valid_moves_player2(square)
    #     else:
    #         if square.ROW - 1 >= 0:
    #             if square.COLUMN - 1 >= 0:
    #                 if self.squares[(square.ROW - 1) * self.COLS + (square.COLUMN - 1)].piece == None:
    #                     moves.append(self.squares[(square.ROW - 1) * self.COLS + (square.COLUMN - 1)])
    #             if square.COLUMN + 1 < self.COLS:
    #                 if self.squares[(square.ROW - 1) * self.COLS + (square.COLUMN + 1)].piece == None:
    #                     moves.append(self.squares[(square.ROW - 1) * self.COLS + (square.COLUMN + 1)])
    #     return moves

    # def get_valid_moves_player2(self, square):
    #     moves = []
    #     if square.piece.king:
    #         moves += self.get_valid_moves_player1(square)
    #     else:
    #         if square.ROW + 1 < self.ROWS:
    #             if square.COLUMN - 1 >= 0:
    #                 if self.squares[(square.ROW + 1) * self.COLS + (square.COLUMN - 1)].piece == None:
    #                     moves.append(self.squares[(square.ROW + 1) * self.COLS + (square.COLUMN - 1)])
    #             if square.COLUMN + 1 < self.COLS:
    #                 if self.squares[(square.ROW + 1) * self.COLS + (square.COLUMN + 1)].piece == None:
    #                     moves.append(self.squares[(square.ROW + 1) * self.COLS + (square.COLUMN + 1)])
    #     return moves

    def movePiece(self, selectedSquare, newSquare):
        if newSquare.piece == None and selectedSquare.piece != None:
            selectedSquare.piece.x = (newSquare.x1 + (newSquare.side_length // 2))
            selectedSquare.piece.y = (newSquare.y1 + (newSquare.side_length // 2))
            newSquare.piece = selectedSquare.piece
            selectedSquare.piece = None
            self.changedSquares.append(selectedSquare)
            self.changedSquares.append(newSquare)
            newSquare.updatePiece(selected=False)
            self.turn = 'player1' if self.turn == 'player2' else 'player2'
            return True
        return False

    def setSelected(self, square):
        if self._selected != None:
            if square != None and self.turn == self._selected.piece.player and square.piece != None:
                if square.piece.player == self._selected.piece.player:
                    self._selected.updatePiece(selected=False)
                    self._selected = square
                    square.updatePiece(selected=True)
                    self.changedSquares.append(self._selected)
                    self.changedSquares.append(square)
            elif square != None and square.piece == None:
                # moves = self.get_valid_moves(self._selected)
                # print(f"Moves: {moves}")
                if self.movePiece(self._selected, square):
                    self._selected.updatePiece(selected=False)
                    self._selected = None
                    self.changedSquares.append(square)
        if square != None and square.piece != None and self.turn == square.piece.player:
            self._selected = square
            square.updatePiece(selected=True)
            self.changedSquares.append(square)
    def draw(self, screen):
        for square in self.squares:
            square.draw(screen)
        self.changedSquares = []


