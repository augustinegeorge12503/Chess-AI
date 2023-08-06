import pygame
from const import *

class Game:

    def __init__(self) -> None:
        pass

    # show methods
    
    def show_bg(self, surface):
        for row in range(ROW):
            for col in range(COL):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)
                
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(surface, color, rect)