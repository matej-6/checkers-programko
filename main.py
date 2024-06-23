import pygame
from Board import Board
import time

BOARD_SIZES = [8, 10, 12]
SCREEN_SIZE = (800, 800)
FPS = 60
FONT_PATH = "edit-undo.brk.ttf"

class Button:
    def __init__(self, pos, text, font, text_color, bg_color, outline_color, border_color):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.bg_color = bg_color
        self.outline_color = outline_color
        self.border_color = border_color
        self.image = self.font.render(self.text, True, self.text_color)
        self.rect = self.image.get_rect(center=pos)
        self.border_width = 3
        self.padding = 20
        self.rect.inflate_ip(self.padding, self.padding)
        self.selected = False

    def draw_border(self, screen):
        if self.selected:
            pygame.draw.rect(screen, self.border_color, self.rect, width=self.border_width)

    def update(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.image, self.image.get_rect(center=self.rect.center))
        self.draw_border(screen)

    def checkForInput(self, position):
        if self.rect.left <= position[0] <= self.rect.right and self.rect.top <= position[1] <= self.rect.bottom:
            return True
        return False

def get_font(size):
    return pygame.font.Font(FONT_PATH, size)

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Checkers")
        self.WIDTH = SCREEN_SIZE[0]
        self.HEIGHT = SCREEN_SIZE[1]
        self.clock = pygame.time.Clock()
        self.rainbow_mode = False
        self.selected_size_button = None
        self.selected_mode_button = None
        self.running = True
        self.end_game = False
        self.winner = None
        self.board = None

    def main_menu(self):
        TITLE_TEXT = get_font(140).render("CHECKERS", True, (255, 255, 255))  
        TITLE_TEXT_RECT = TITLE_TEXT.get_rect(center=(self.WIDTH // 2, 100))
        SIZE_TEXT = get_font(70).render("DIFFICULTY", True, (255, 255, 255))  
        SIZE_TEXT_RECT = SIZE_TEXT.get_rect(center=(self.WIDTH // 2, 250))
        button_easy = Button((200, 350), 'EASY', get_font(60), 'white', '#f72585', '#343a40', '#ffffff')  
        button_medium = Button((400, 350), 'MEDIUM', get_font(60), 'white', '#f72585', '#343a40', '#ffffff')  
        button_hard = Button((600, 350), 'HARD', get_font(60), 'white', '#f72585', '#343a40', '#ffffff')  
        size_buttons = [button_easy, button_medium, button_hard]
        MODE_TEXT = get_font(70).render("GAME MODE", True, (255, 255, 255))  
        MODE_TEXT_RECT = MODE_TEXT.get_rect(center=(self.WIDTH // 2, 450))
        button_2p = Button((350, 550), '2P', get_font(60), 'white', '#f72585', '#343a40', '#ffffff')  
        button_ai = Button((450, 550), 'AI', get_font(60), 'white', '#f72585', '#343a40', '#ffffff')  
        game_mode_buttons = [button_2p, button_ai]

        start_button = Button((self.WIDTH // 2, 700), 'START', get_font(80), 'white', '#4CAF50', '#343a40', '#ffffff')  

        while self.running:
            self.SCREEN.fill('#212529')
            MOUSE_POSITION = pygame.mouse.get_pos()

            self.SCREEN.blit(TITLE_TEXT, TITLE_TEXT_RECT)

            self.SCREEN.blit(SIZE_TEXT, SIZE_TEXT_RECT)
            for button in size_buttons:
                button.update(self.SCREEN)

            self.SCREEN.blit(MODE_TEXT, MODE_TEXT_RECT)
            for button in game_mode_buttons:
                button.update(self.SCREEN)

            start_button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in size_buttons:
                        if button.checkForInput(MOUSE_POSITION):
                            if self.selected_size_button is not None:
                                self.selected_size_button.selected = False
                            button.selected = True
                            self.selected_size_button = button
                            if button.text == 'EASY':
                                self.selected_size = BOARD_SIZES[0]
                            elif button.text == 'MEDIUM':
                                self.selected_size = BOARD_SIZES[1]
                            elif button.text == 'HARD':
                                self.selected_size = BOARD_SIZES[2]

                    for button in game_mode_buttons:
                        if button.checkForInput(MOUSE_POSITION):
                            if self.selected_mode_button is not None:
                                self.selected_mode_button.selected = False
                            button.selected = True
                            self.selected_mode_button = button
                            if button.text == 'AI':
                                self.selected_mode = 'AI'
                            else:
                                self.selected_mode = '2P'

                    if start_button.rect.collidepoint(MOUSE_POSITION):
                        if hasattr(self, 'selected_size') and hasattr(self, 'selected_mode'):
                            self.play(self.selected_size, self.selected_mode)
                            return

            pygame.display.update()
            self.clock.tick(FPS)

    def play(self, board_size, game_mode):
        if(game_mode == "AI"):
            self.board = Board(board_size, board_size, True)
        else:
            self.board = Board(board_size, board_size)
        self.running = True
        self.end_game = False
        self.winner = None
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and (self.board.turn == 'player2' or not self.board.aiPlayer):
                    pos = pygame.mouse.get_pos()
                    if not self.end_game:
                        square = self.board.find_square_by_pos(pos)
                        self.board.setSelected(square)
            if self.board.aiPlayer and self.board.turn == 'player1' and not self.end_game:
                self.board.ai_move()


            self.SCREEN.fill((0, 0, 0))
            if not self.end_game:
                self.board.draw(self.SCREEN)
                self.winner = self.board.check_winner()
                if self.winner:
                    self.end_game = True
            else:
                self.win_screen()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
    def win_screen(self):
        self.SCREEN.fill('#212529')
        MOUSE_POSITION = pygame.mouse.get_pos()
        WIN_TEXT = get_font(100).render(f'{self.winner} wins!', True, (255, 255, 255))
        WIN_TEXT_RECT = WIN_TEXT.get_rect(center=(self.WIDTH // 2, 200))
        self.SCREEN.blit(WIN_TEXT, WIN_TEXT_RECT)
        SCORE_TEXT = get_font(30).render(f'Score: Player 1 - {self.board.player1_left} | Player 2 - {self.board.player2_left}', True, (255, 255, 255))
        SCORE_TEXT_RECT = SCORE_TEXT.get_rect(center=(self.WIDTH // 2, 300))
        self.SCREEN.blit(SCORE_TEXT, SCORE_TEXT_RECT)
        self.restart_button = Button((self.WIDTH // 2, 400), 'RESTART', get_font(50), 'white', '#4CAF50', '#343a40', '#ffffff')
        self.main_menu_button = Button((self.WIDTH // 2, 500), 'MAIN MENU', get_font(50), 'white', '#f72585', '#343a40', '#ffffff')
        self.restart_button.update(self.SCREEN)
        self.main_menu_button.update(self.SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button.checkForInput(MOUSE_POSITION):
                    self.play(self.board.rows, self.selected_mode)
                    return
                elif self.main_menu_button.checkForInput(MOUSE_POSITION):
                    self.main_menu()
                    return
        pygame.display.update()
        self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.main_menu()

