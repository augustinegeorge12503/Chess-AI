import pygame
from const import *

class Design:

    def __init__(self) -> None:
        self.background = None
        self.color = (255,255,255)
        self.big_font = pygame.font.Font(f'assets/menu/font/vermin_vibes.otf', 50)
        self.small_font = pygame.font.Font(f'assets/menu/font/vermin_vibes.otf', 20)
        self.set_background('starry')

    # show functions
    def show_background(self, surface):
        surface.blit(self.background, (0,0))
    
    def show_text(self, font, text, centerx, centery, surface):

        text = font.render(text, True, self.color)
        rect = text.get_rect()
        rect.center = (centerx, centery)
        surface.blit(text, rect)
    
    def show_page(self, page, surface):
        self.show_background(surface)

        # home page
        if page == 'home':
            self.show_text(self.big_font, 'ChessNow', 400, 100, surface)

        elif page == 'key':
            self.show_text(self.small_font, 'Escape:  Go Back', 400, 300, surface)
            self.show_text(self.small_font, 'R:  Reset Board', 400, 400, surface)
            self.show_text(self.small_font, 'Z:  Change Theme', 400, 500, surface)

    # set methods
    def set_background(self, bg_name):
        image = pygame.transform.scale(pygame.image.load(f'assets/menu/background/{bg_name}.jpg'), (WIDTH, HEIGHT))
        self.background = image        
    
