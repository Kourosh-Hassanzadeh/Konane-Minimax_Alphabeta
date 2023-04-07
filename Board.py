
from Tile import Tile

class KonaneError(AttributeError):
    """
    This class is used to indicate a problem in the konane game.
    """

class Board():
    def __init__(self, size, init_board):
        self.size = size
        self.game_board = init_board


    def valid(self, row, col):
        """
        Returns true if the given row and col represent a valid location on
        the konane board.
        """
        return row >= 0 and col >= 0 and row < self.size and col < self.size


    def distance(self, r1, c1, r2, c2):
        """
        Returns the distance between two points in a vertical or
        horizontal line on the konane board. Diagonal jumps are NOT
        allowed.
        """
        return abs(r1-r2 + c1-c2)


    def count_symbol(self, symbol):
        """
        Returns the number of instances of the symbol on the board.
        """
        count = 0
        for r in range(self.size):
            for c in range(self.size):
                if self.game_board[r][c].piece == symbol:
                    count += 1
        return count


    def contains(self, row, col, symbol):
        """
        Returns true if the given row and col represent a valid location on
        the konane board and that location contains the given symbol.
        """
        return self.valid(row,col) and self.game_board[row][col].piece == symbol



