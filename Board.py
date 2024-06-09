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

        print(self.squares)

    def initiatePieces(self):
        for i in range(0, 3):
            for j in range(0, self.COLS):
                if self.squares[j*self.COLS+i].color == (139, 120, 109):
                    self.squares[j*self.COLS+i].initiatePiece((235, 245, 238), 'player1')
                    # self.changedSquares.append(self.squares[j*self.COLS+i])

        for i in range(5, 8):
            for j in range(0, self.COLS):
                if self.squares[j*self.COLS+i].color == (139, 120, 109):
                    self.squares[j*self.COLS+i].initiatePiece((100, 120, 109), 'player2')
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
        moves = {}
        if square.piece:
            if square.piece.player == 'player1' or square.piece.king:
                moves.update(self.traverse_bottom_left(square))
                moves.update(self.traverse_bottom_right(square))
            if square.piece.player == 'player2' or square.piece.king:
                moves.update(self.traverse_top_left(square))
                moves.update(self.traverse_top_right(square))
        return moves

    def traverse_bottom_left(self, square, jumped=[]):
        moves = {}
        if square.ROW == self.ROWS - 1 or square.COLUMN == 0:
            return moves
        square_index = self.squares.index(square)
        bottom_left_index = square_index - self.COLS + 1
        if 0 <= bottom_left_index < len(self.squares):
            bottom_left_square = self.squares[bottom_left_index]
            if bottom_left_square.piece is None:
                moves[bottom_left_square] = jumped
            elif bottom_left_square.piece.player != square.piece.player:
                moves.update(self.traverse_bottom_left(bottom_left_square, jumped + [bottom_left_square]))

        return moves

    def traverse_bottom_right(self, square, jumped=[]):
        moves = {}
        if square.ROW == self.ROWS - 1 or square.COLUMN == self.COLS - 1:
            return moves
        square_index = self.squares.index(square)
        bottom_right_index = square_index + self.COLS + 1
        if 0 <= bottom_right_index < len(self.squares):
            bottom_right_square = self.squares[bottom_right_index]
            if bottom_right_square.piece is None:
                moves[bottom_right_square] = jumped
            elif bottom_right_square.piece.player != square.piece.player:
                moves.update(self.traverse_bottom_right(bottom_right_square, jumped + [bottom_right_square]))

        return moves


    def traverse_top_left(self, square, jumped=[]):
        moves = {}
        if square.ROW == 0 or square.COLUMN == 0:
            return moves
        square_index = self.squares.index(square)
        top_left_index = square_index - self.COLS - 1
        if 0 <= top_left_index < len(self.squares):
            top_left_square = self.squares[top_left_index]
            if top_left_square.piece is None:
                moves[top_left_square] = jumped
            elif square.piece and (top_left_square.piece.player != self.turn):
                moves.update(self.traverse_top_left(top_left_square, jumped + [top_left_square]))

        return moves



    def traverse_top_right(self, square, jumped=[]):
        moves = {}
        if square.ROW == 0 or square.COLUMN == self.COLS - 1:
            return moves
        square_index = self.squares.index(square)
        top_right_index = square_index + self.COLS - 1
        if 0 <= top_right_index < len(self.squares):
            top_right_square = self.squares[top_right_index]
            if top_right_square.piece is None:
                moves[top_right_square] = jumped
            elif square.piece and (top_right_square.piece.player != self.turn):
                moves.update(self.traverse_top_right(top_right_square, jumped + [top_right_square]))

        return moves
    # def get_valid_moves_player1(self, square):
    #     moves = []
    #     # if square.piece.king:
    #     #     moves += self.get_valid_moves_player2(square)
    #
    #     squareIndex = self.squares.index(square)
    #
    #     if square.ROW < self.ROWS - 1:
    #         if square.COLUMN > 0:
    #             if self.squares[squareIndex - self.COLS + 1].piece == None:
    #                 moves.append(self.squares[squareIndex - self.COLS + 1])
    #         if square.COLUMN < self.COLS - 1:
    #             if self.squares[squareIndex + self.COLS + 1].piece == None:
    #                 moves.append(self.squares[squareIndex + self.COLS + 1])
    #
    #     return moves
    #
    # def get_valid_moves_player2(self, square):
    #     moves = []
    #     currentSquareIndex = self.squares.index(square)
    #     directions = [currentSquareIndex - self.COLS - 1, currentSquareIndex + self.COLS - 1]
    #
    #     if square.piece.king:
    #         directions += [currentSquareIndex - self.COLS + 1, currentSquareIndex + self.COLS + 1]
    #
    #     for direction in directions:
    #         self._explore_moves(direction, square, currentSquareIndex, moves)
    #
    #     return moves
    #
    # def _explore_moves(self, direction, square, currentSquareIndex, moves, jumped=[]):
    #     if 0 <= direction < len(self.squares):
    #         next_square = self.squares[direction]
    #         if next_square.piece is None:
    #             moves.append(next_square)
    #         elif next_square.piece.player != square.piece.player:
    #             direction_row_diff = direction // self.COLS - currentSquareIndex // self.COLS
    #             direction_col_diff = direction % self.COLS - currentSquareIndex % self.COLS
    #             jump_square_index = direction + direction_row_diff * self.COLS + direction_col_diff
    #
    #             if 0 <= jump_square_index < len(self.squares) and abs(
    #                     jump_square_index // self.COLS - direction // self.COLS) == 1 and abs(
    #                     jump_square_index % self.COLS - direction % self.COLS) == 1:
    #                 jump_square = self.squares[jump_square_index]
    #                 if jump_square.piece is None and jump_square not in jumped:
    #                     moves.append(jump_square)
    #                     self._explore_moves(jump_square_index, jump_square, direction, moves, jumped + [next_square])

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

    def movePiece(self, selectedSquare, newSquare, jumpedItems):
        print(f"Selected square: {selectedSquare}")
        print(f"New square: {newSquare}")
        print(f"Jumped items: {jumpedItems}")
        if jumpedItems:
            for jumpedItem in jumpedItems:
                if jumpedItem.piece.player == 'player1':
                    self.player1_left -= 1
                else:
                    self.player2_left -= 1
                jumpedItem.piece = None
                self.changedSquares.append(jumpedItem)

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
                    for s in self.squares:
                        s.set_valid_move(valid=False)
                    self._selected = square
                    square.updatePiece(selected=True)
                    self.changedSquares.append(self._selected)
                    self.changedSquares.append(square)
            elif square != None and square.piece == None and square in self.get_valid_moves(self._selected):
                if self.movePiece(self._selected, square, self.get_valid_moves(self._selected)[square]):
                    self._selected.updatePiece(selected=False)
                    for s in self.squares:
                        s.set_valid_move(valid=False)
                    self._selected = None
                    self.changedSquares.append(square)
        if square != None and square.piece != None and self.turn == square.piece.player:
            self._selected = square
            square.updatePiece(selected=True)
            moves = self.get_valid_moves(square)
            for square in moves:
                square.set_valid_move()
            print(moves)
            self.changedSquares.append(square)
    def draw(self, screen):
        for square in self.squares:
            square.draw(screen)
        self.changedSquares = []


