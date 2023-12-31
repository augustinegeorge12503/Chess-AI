import pygame
from sys import exit
from const import *
from game import Game
from square import Square
from move import Move
from page import Page
from design import Design
from button import Button

class Main:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('ChessNow')
        self.game = Game()
        self.page = Page()
        self.design = Design()

    def mainloop(self):
        
        
        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board
        page = self.page
        design = self.design
        
        while True:

            # home page
            if page.current_page == 'home':

                design.show_page('home', screen)

                # play button
                play_button = Button('Play', design.small_font, (0,0,0), (255,255,255), (180, 50), (400,350), screen)
                play_button.draw()

                # key button
                key_button = Button('Key', design.small_font, (0,0,0), (255,255,255), (180, 50), (400,450), screen)
                key_button.draw()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if play_button.check_collision():
                            page.change_page('pvp')
                        elif key_button.check_collision():
                            page.change_page('key')

            # key page
            if page.current_page == 'key':
                
                design.show_page('key', screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            page.change_page('home')
                        
            # pvp page
            if page.current_page == 'pvp':
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
                                # play sound
                                captured = board.squares[released_row][released_col].has_piece()
                                game.play_sound(captured)

                                board.move(dragger.piece, move)
                                game.next_turn()

                        dragger.undrag_piece()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z:
                            game.change_theme()
                            
                        if event.key == pygame.K_r:
                            self.game.reset()
                            game = self.game
                            dragger = self.game.dragger
                            board = self.game.board

                        if event.key == pygame.K_ESCAPE:
                            page.change_page('home')

                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
            
            # update screen
            pygame.display.flip()

main = Main()
main.mainloop()