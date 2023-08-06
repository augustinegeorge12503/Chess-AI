from const import *
from square import Square

class Board:

    def __init__(self) -> None:
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COL)]

        self._create()


    def _create(self):
        for row in range(ROW):
            for col in range(COL):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        pass