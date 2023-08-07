import pygame
from sys import exit
from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('ChessNow')
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board
        
        while True:

            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece

                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                elif event.type == pygame.MOUSEMOTION:
                    hover_row = event.pos[1] // SQSIZE
                    hover_col = event.pos[0] // SQSIZE
                    game.set_hover(hover_row, hover_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:    

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)

                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            game.next_turn()

                    dragger.undrag_piece()


                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            pygame.display.flip()

main = Main()
main.mainloop()