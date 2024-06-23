import random

import pygame
from Square import Square

class Board:
    def __init__(self, cols=8, rows=8):
    def __init__(self, cols=8, rows=8, pocet_figuriek=8, aiPlayer=False):
        self.COLS = cols
        self.ROWS = rows
        self.squares = []
        self.aiPlayer = aiPlayer
        self.turn = 'player2'
        self.player1_left = self.player2_left = self.calculate_pocet_figuriek(cols)
        self.changedSquares = []
        self._selected = None
        self.player1_piece_image = pygame.transform.scale(pygame.image.load('assets/images/whitePiece.png'), (int(650 / self.ROWS), int(650 / self.ROWS)))
        self.player2_piece_image = pygame.transform.scale(pygame.image.load('assets/images/blackPiece.png'), (int(650 / self.ROWS), int(650 / self.ROWS)))
        self.player1_king_image = pygame.transform.scale(pygame.image.load('assets/images/kingWhitePiece.png'), (int(650 / self.ROWS), int(650 / self.ROWS)))
        self.player2_king_image = pygame.transform.scale(pygame.image.load('assets/images/kingBlackPiece.png'), (int(650 / self.ROWS), int(650 / self.ROWS)))
        self.initiateSquares()
        self.initiatePieces()
        if self.aiPlayer:
            print("AI is playing")

    def calculate_pocet_figuriek(self, cols):
        if cols == 8:
            return 12
        elif cols == 10:
            return 15
        elif cols == 12:
            return 18
        else:
            raise ValueError("Unsupported board size")

    def initiateSquares(self):
        for i in range(self.COLS):
            for j in range(self.ROWS):
                color = (235, 245, 238) if (i + j) % 2 == 0 else (139, 120, 109)
                new_square = Square(800 / self.COLS, color, i * (800 / self.COLS), j * (800 / self.ROWS), j, i)
                self.squares.append(new_square)
                self.changedSquares.append(new_square)

    def initiatePieces(self):
        radius = 350 / self.ROWS
        for i in range(3):
            for j in range(self.COLS):
                square = self.squares[j * self.COLS + i]
                if square.color == (139, 120, 109):
                    square.initiatePiece((235, 245, 238), 'player1', radius, self.player1_piece_image, self.player1_king_image)

        for i in range(self.ROWS - 3, self.ROWS):
            for j in range(self.COLS):
                square = self.squares[j * self.COLS + i]
                if square.color == (139, 120, 109):
                    square.initiatePiece((100, 120, 109), 'player2', radius, self.player2_piece_image, self.player2_king_image)

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

    def get_all_valid_moves(self):
        moves = {}
        for square in self.squares:
            temp_moves = {}
            if square.piece and square.piece.player == self.turn:
                temp_moves.update(self.get_valid_moves(square))
                if temp_moves:
                    moves[square] = temp_moves
        return moves

    def ai_move(self):
        valid_moves = self.get_all_valid_moves()
        print(valid_moves)


        if valid_moves:
            # Select a random source square with a valid move
            source_square, moves_dict = random.choice(list(valid_moves.items()))

            print('Selected source square:', source_square)

            # Select a random destination square from the possible moves
            if moves_dict:
                destination_square = random.choice(list(moves_dict.keys()))
                move_data = moves_dict[destination_square]

                print('Selected destination square:', destination_square)
                print('Move data:', move_data)

                # Execute the move
                self.movePiece(source_square, destination_square, move_data)

                # Change the turn to the other player
            else:
                print('No valid moves available for the selected source square.')
        else:
            print('No valid moves available.')

        self.turn = 'player2'  # Assuming 'player1' is the other player

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



    def check_if_piece_became_king(self, square):
        if square.piece:
            if square.piece.player == 'player1' and square.ROW == self.ROWS - 1:
                square.piece.king = True
                print("Player 1 became king")
            elif square.piece.player == 'player2' and square.ROW == 0:
                square.piece.king = True
                print("Player 2 became king")


    def movePiece(self, selectedSquare, newSquare, jumpedItems):
        if jumpedItems:
            for jumpedItem in jumpedItems:
                if jumpedItem.piece and jumpedItem.piece.player == 'player1':
                    self.player1_left -= 1
                    print (self.player1_left)
                elif jumpedItem.piece and jumpedItem.piece.player == 'player2':
                    self.player2_left -= 1
                    print(self.player2_left)
                jumpedItem.piece = None
                self.changedSquares.append(jumpedItem)

        if newSquare.piece is None and selectedSquare.piece is not None:
            selectedSquare.piece.x = newSquare.x1 + (newSquare.side_length // 2)
            selectedSquare.piece.y = newSquare.y1 + (newSquare.side_length // 2)
            newSquare.piece = selectedSquare.piece
            selectedSquare.piece = None
            self.changedSquares.append(selectedSquare)
            self.changedSquares.append(newSquare)
            newSquare.updatePiece(selected=False)
            self.turn = 'player1' if self.turn == 'player2' else 'player2'
            self.check_if_piece_became_king(newSquare)
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



    def check_winner(self):
        if self.player1_left <= 0:
            return 'player2'
        elif self.player2_left <= 0:
            return 'player1'
        return None
    
    

