import pygame
from Board import Board  

BOARD_SIZES = [8, 10, 12]
SCREEN_SIZE = (800, 800)
FPS = 60
FONT_PATH = "edit-undo.brk.ttf"

class Button:
    def __init__(self, pos, text, font, text_color, bg_color, outline_color, border_color):
        self.text = text
        self.font = font
        self.text_color = pygame.Color(text_color)
        self.bg_color = pygame.Color(bg_color)
        self.outline_color = pygame.Color(outline_color)
        self.border_color = pygame.Color(border_color)
        self.image = self.font.render(self.text, True, self.text_color)
        self.rect = self.image.get_rect(center=pos)
        self.rect.inflate_ip(20, 20)  
        self.selected = False

    def draw_border(self, screen):
        if self.selected:
            pygame.draw.rect(screen, self.border_color, self.rect, width=3)

    def update(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        screen.blit(self.image, self.image.get_rect(center=self.rect.center))
        self.draw_border(screen)

    def check_for_input(self, position):
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
        self.selected_size_button = None
        self.selected_mode_button = None
        self.selected_size = None  
        self.selected_mode = None  

    def main_menu(self):
        TITLE_TEXT = get_font(140).render("CHECKERS", True, pygame.Color('white'))
        TITLE_TEXT_RECT = TITLE_TEXT.get_rect(center=(self.WIDTH // 2, 120))
        SIZE_TEXT = get_font(70).render("DIFFICULTY", True, pygame.Color('white'))
        SIZE_TEXT_RECT = SIZE_TEXT.get_rect(center=(self.WIDTH // 2, 250))
        button_easy = Button((200, 350), 'EASY', get_font(60), 'white', '#f72585', '#343a40', '#ffffff')
        button_medium = Button((400, 350), 'MEDIUM', get_font(60), 'white', '#f72585', '#343a40', '#ffffff')
        button_hard = Button((600, 350), 'HARD', get_font(60), 'white', '#f72585', '#343a40', '#ffffff')
        MODE_TEXT = get_font(70).render("GAME MODE", True, pygame.Color('white'))
        MODE_TEXT_RECT = MODE_TEXT.get_rect(center=(self.WIDTH // 2, 450))
        button_2p = Button((350, 550), '2P', get_font(60), 'white', '#f72585', '#343a40', '#ffffff')
        button_ai = Button((450, 550), 'AI', get_font(60), 'white', '#f72585', '#343a40', '#ffffff')
        start_button = Button((self.WIDTH // 2, 700), 'START', get_font(80), 'white', '#4CAF50', '#343a40', '#ffffff')

        while True:
            self.SCREEN.fill(pygame.Color('#212529'))
            MOUSE_POSITION = pygame.mouse.get_pos()
            self.SCREEN.blit(TITLE_TEXT, TITLE_TEXT_RECT)
            self.SCREEN.blit(SIZE_TEXT, SIZE_TEXT_RECT)
            for button in [button_easy, button_medium, button_hard]:
                button.update(self.SCREEN)

            self.SCREEN.blit(MODE_TEXT, MODE_TEXT_RECT)
            for button in [button_2p, button_ai]:
                button.update(self.SCREEN)

            start_button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in [button_easy, button_medium, button_hard]:
                        if button.check_for_input(MOUSE_POSITION):
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
                    if start_button.check_for_input(MOUSE_POSITION):
                            self.play(self.selected_size, self.selected_mode)
                            return

            pygame.display.update()
            self.clock.tick(FPS)

    def play(self, board_size, game_mode):
        board = Board(board_size, board_size, board_size)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    square = board.find_square_by_pos(pos)
                    board.set_selected(square)

            self.SCREEN.fill(pygame.Color(0, 0, 0))
            board.draw(self.SCREEN)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.main_menu()
