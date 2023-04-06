import copy
from Tile import Tile

class KonaneError(AttributeError):
    """
    This class is used to indicate a problem in the konane game.
    """

class Board():
    def __init__(self, size):
        self.size = size

    def initialize_board(self):
        board = []
        tile = Tile(2,0,0,0)
        for i in range(self.size):
            row_gui = []
            for j in range(self.size):
                row_gui.append(tile)
                tile = Tile(3-tile.piece, tile.outline, i, j+1)
            board.append(row_gui)
            if self.size%2 == 0:
                tile = Tile(3-tile.piece, tile.outline, i+1, 0)

        return board

    def next_board(self, board, player, move):
        """
        Given a move for a particular player from (r1,c1) to (r2,c2) this
        executes the move on a copy of the current konane board.  It will
        raise a KonaneError if the move is invalid. It returns the copy of
        the board, and does not change the given board.
        """
        r1 = move[0]
        c1 = move[1]
        r2 = move[2]
        c2 = move[3]

        next = copy.deepcopy(board)
        if not (self.valid(r1, c1) and self.valid(r2, c2)):
            raise KonaneError
        
        if next[r1][c1].piece != player:
            raise KonaneError
        dist = self.distance(r1, c1, r2, c2)
        if dist == 0:
            if self.opening_move(board):
                next[r1][c1].piece = Tile.P_NONE
                return next
            raise KonaneError
        if next[r2][c2].piece != Tile.P_NONE:
            raise KonaneError
        jumps = dist/2
        dr = int((r2 - r1)/dist)
        dc = int((c2 - c1)/dist)
        for i in range(int(jumps)):
            #test
            if next[r1+dr][c1+dc].piece != self.opponent(player):
                raise KonaneError
            next[r1][c1].piece = Tile.P_NONE
            next[r1+dr][c1+dc].piece = Tile.P_NONE
            r1 += 2*dr
            c1 += 2*dc
            next[r1][c1].piece = player
        return next


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


    def opening_move(self, board):
        return self.count_symbol(board, Tile.P_NONE) <= 1
            

    def count_symbol(self, board, symbol):
        """
        Returns the number of instances of the symbol on the board.
        """
        count = 0
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c].piece == symbol:
                    count += 1
        return count



    def generate_all_possible_moves(self, board, player):
        """
        Generates and returns all legal moves for the given player using the
        current board configuration.
        """
        if self.opening_move(board):
            if player== Tile.P_Black:
                return self.generate_first_moves(board)
            else:
                return self.generate_second_moves(board)
        else:
            moves = []
            rd = [-1,0,1,0]
            cd = [0,1,0,-1]
            for r in range(self.size):
                for c in range(self.size):
                    if board[r][c].piece == player:
                        for i in range(len(rd)):
                            moves += self.check(board,r,c,rd[i],cd[i],1,
                                                self.opponent(player))
            return moves
        

    def generate_first_moves(self, board):
        """
        Returns the special cases for the first move of the game.
        """
        moves = []
        moves.append([0]*4)
        moves.append([self.size-1]*4)
        moves.append([self.size//2]*4)
        moves.append([(self.size//2)-1]*4)
        return moves

    def generate_second_moves(self, board):
        """
        Returns the special cases for the second move of the game, based
        on where the first move occurred.
        """
        moves = []
        if board[0][0].piece == Tile.P_NONE:
            moves.append([0,1]*2)
            moves.append([1,0]*2)
            return moves
        elif board[self.size-1][self.size-1].piece == Tile.P_NONE:
            moves.append([self.size-1,self.size-2]*2)
            moves.append([self.size-2,self.size-1]*2)
            return moves
        elif board[self.size//2-1][self.size//2-1].piece == Tile.P_NONE:
            pos = self.size//2 -1
        else:
            pos = self.size//2
        moves.append([pos,pos-1]*2)
        moves.append([pos+1,pos]*2)
        moves.append([pos,pos+1]*2)
        moves.append([pos-1,pos]*2)
        return moves


    def check(self, board, r, c, rd, cd, factor, opponent):
        """
        Checks whether a jump is possible starting at (r,c) and going in the
        direction determined by the row delta (rd), and the column delta (cd).
        The factor is used to recursively check for multiple jumps in the same
        direction.  Returns all possible jumps in the given direction.
        """
        if self.contains(board,r+factor*rd,c+factor*cd,opponent) and \
           self.contains(board,r+(factor+1)*rd,c+(factor+1)*cd, Tile.P_NONE):
            return [[r,c,r+(factor+1)*rd,c+(factor+1)*cd]] + \
                   self.check(board,r,c,rd,cd,factor+2,opponent)
        else:
            return []


    def contains(self, board, row, col, symbol):
        """
        Returns true if the given row and col represent a valid location on
        the konane board and that location contains the given symbol.
        """
        return self.valid(row,col) and board[row][col].piece == symbol


    def opponent(self, tile):
        """
        Given a player symbol, returns the opponent's symbol, 'B' for black,
        or 'W' for white.  (3 - color)
        """
        return Tile.P_Black if tile == Tile.P_White else Tile.P_White
