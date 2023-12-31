from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self) -> None:
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COL)]
        self.last_move = None

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')


    def _create(self):
        for row in range(ROW):
            for col in range(COL):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawn
        for col in range(COL):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
        # knight
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishop
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rook
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    
    def calc_moves(self, piece, row, col):
        '''
            calculate all the possible move for a specific at a specific position
        '''

        def pawn_moves():
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(move_row, col)

                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        break
                else:
                    break
            
            # diagonal moves
            move_row = row + piece.dir
            move_cols = [col - 1, col + 1]
            for move_col in move_cols:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)

                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves():
            possible_moves = [
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row - 1, col + 2),
                (row - 1, col - 2),
                (row + 2, col - 1),
                (row + 2, col + 1),
                (row + 1, col - 2),
                (row + 1, col + 2)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        move = Move(initial, final)
                        piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                move_row = row + row_incr
                move_col = col + col_incr
            
                while True:
                    if Square.in_range(move_row, move_col):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)

                        move = Move(initial, final)

                        if self.squares[move_row][move_col].isempty():
                            piece.add_move(move)
                        if self.squares[move_row][move_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break
                        if self.squares[move_row][move_col].has_team_piece(piece.color):
                            break

                        move_row += row_incr
                        move_col += col_incr
                    else: break

        def king_moves():
            possible_moves = [
                (row - 1, col - 1),
                (row - 1, col),
                (row - 1, col + 1),
                (row, col - 1),
                (row, col + 1),
                (row + 1, col - 1),
                (row + 1, col),
                (row + 1, col + 1)
            ]

            for possible_move in possible_moves:
                move_row, move_col = possible_move
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(move_row, move_col)

                        move = Move(initial, final)
                        piece.add_move(move)

        if isinstance(piece, Pawn):
            pawn_moves()         
        elif isinstance(piece, Knight): 
            knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves([(-1,-1), (-1,1), (1,-1), (1,1)])
        elif isinstance(piece, Rook): 
            straightline_moves([(1,0), (-1,0), (0,1), (0,-1)])
        elif isinstance(piece, Queen): 
            straightline_moves([(-1,-1), (-1,1), (1,-1), (1,1), (1,0), (-1,0), (0,1), (0,-1)])
            # combination of rook and bishop
        elif isinstance(piece, King): 
            king_moves()
        
    def move(self, piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece 

        piece.moved = True
        piece.clear_moves()
        self.last_move = move

    def valid_move(self, piece, move): 
        return move in piece.moves