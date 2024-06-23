import pygame

class Piece:
    def __init__(self, color, x, y, player, radius, image, king_image):
        self.color = color
        self.x = x
        self.y = y
        self.king = False
        self.player = player
        self.selected = False
        self.radius = radius
        self.image = image
        self.king_image = king_image

    def draw(self, screen):
        piece_image = self.king_image if self.king else self.image
        rect = piece_image.get_rect(center=(self.x, self.y))
        screen.blit(piece_image, rect)
        if self.selected:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius, 3)

    def __str__(self):
        return f"Piece at {self.x}, {self.y} with color {self.color} and player {self.player}"

