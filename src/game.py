import pygame
from const import *
from board import Board
from dragger import Dragger

class Game:

    def __init__(self) -> None:
        self.board = Board()
        self.dragger = Dragger()

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
    
    def show_pieces(self, surface):
        for row in range(ROW):
            for col in range(COL):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        image = piece.texture
                        image_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE //2
                        piece.texture_rect = image.get_rect(center=image_center)
                        surface.blit(image, piece.texture_rect) 
    
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646' 
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)