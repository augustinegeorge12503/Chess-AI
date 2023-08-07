import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:

    def __init__(self) -> None:
        self.next_player = 'white'
        self.hovered_square = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # show methods
    
    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROW):
            for col in range(COL):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(surface, color, rect)

                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    label = self.config.font.render(str(ROW - row), 1, color)
                    label_pos = (5, 5 + row * SQSIZE)
                    surface.blit(label, label_pos)

                if row == 7:
                    color = theme.bg.light if col % 2 == 0 else theme.bg.dark
                    label = self.config.font.render(Square.get_alphacol(col), 1, color)
                    label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(label, label_pos)

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
        theme  = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark 
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_square:
            color = (180,180,180)
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)
    
    # other methods

    def next_turn(self):
        self.next_player = 'black' if self.next_player == 'white' else 'white'

    def set_hover(self, row, col):
        if Square.in_range(row, col):
            self.hovered_square = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()
    
    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    
    def reset(self):
        self.__init__('')