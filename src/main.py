import pygame
from sys import exit
from const import *
from game import Game

class Main:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('ChessNow')
        self.game = Game()

    def mainloop(self):
        
        while True:

            self.game.show_bg(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            pygame.display.flip()

main = Main()
main.mainloop()