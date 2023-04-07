from Tile import Tile
import copy

class GameManager:
    def __init__(self):
        NotImplemented


    def next_move(self, board, player, move):
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
        if not (board.valid(r1, c1) and board.valid(r2, c2)):
            raise KonaneError
        
        if next.game_board[r1][c1].piece != player:
            raise KonaneError
        dist = board.distance(r1, c1, r2, c2)
        if dist == 0:
            if self.is_opening_move(board):
                next.game_board[r1][c1].piece = Tile.P_NONE
                return next
            raise KonaneError
        if next.game_board[r2][c2].piece != Tile.P_NONE:
            raise KonaneError
        jumps = dist/2
        dr = int((r2 - r1)/dist)
        dc = int((c2 - c1)/dist)
        for i in range(int(jumps)):
            #test
            if next.game_board[r1+dr][c1+dc].piece != (3-player):
                raise KonaneError
            next.game_board[r1][c1].piece = Tile.P_NONE
            next.game_board[r1+dr][c1+dc].piece = Tile.P_NONE
            r1 += 2*dr
            c1 += 2*dc
            next.game_board[r1][c1].piece = player
        return next


    def is_opening_move(self, board):
        return board.count_symbol(Tile.P_NONE) <= 1
            

    def generate_all_possible_moves(self, board, player):
        """
        Generates and returns all legal moves for the given player using the
        current board configuration.
        """
        if self.is_opening_move(board):
            if player== Tile.P_Black:
                return self.generate_first_moves(board)
            else:
                return self.generate_second_moves(board)
        else:
            moves = []
            rd = [-1,0,1,0]
            cd = [0,1,0,-1]
            for r in range(board.size):
                for c in range(board.size):
                    if board.game_board[r][c].piece == player:
                        for i in range(len(rd)):
                            moves += self.check(board, r,c,rd[i],cd[i],1,
                                                self.opponent(player))
            return moves
        

    def generate_first_moves(self, board):
        """
        Returns the special cases for the first move of the game.
        """
        moves = []
        moves.append([0]*4)
        moves.append([board.size-1]*4)
        moves.append([board.size//2]*4)
        moves.append([(board.size//2)-1]*4)
        return moves


    def generate_second_moves(self, board):
        """
        Returns the special cases for the second move of the game, based
        on where the first move occurred.
        """
        moves = []
        if board.game_board[0][0].piece == Tile.P_NONE:
            moves.append([0,1]*2)
            moves.append([1,0]*2)
            return moves
        elif board.game_board[board.size-1][board.size-1].piece == Tile.P_NONE:
            moves.append([board.size-1,board.size-2]*2)
            moves.append([board.size-2,board.size-1]*2)
            return moves
        elif board.game_board[board.size//2-1][board.size//2-1].piece == Tile.P_NONE:
            pos = board.size//2 -1
        else:
            pos = board.size//2
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
        if board.contains(r+factor*rd,c+factor*cd,opponent) and \
           board.contains(r+(factor+1)*rd,c+(factor+1)*cd, Tile.P_NONE):
            return [[r,c,r+(factor+1)*rd,c+(factor+1)*cd]] + \
                   self.check(board, r,c,rd,cd,factor+2,opponent)
        else:
            return []


    def get_moves_at_tile(self, board, tile, player):
        moves =  self.generate_all_possible_moves(board, player)
        valid_moves_at_tile = []
        print(moves)
        for move in moves:
            if move[0] == tile.row and move[1] == tile.col:
                valid_tile = board.game_board[move[2]][move[3]]
                valid_moves_at_tile.append(valid_tile)
        return valid_moves_at_tile
    

    def find_winner(self, board, color):
        valid_moves = self.generate_all_possible_moves(board, color)

        if valid_moves == []:
            winner = (Tile.P_Black if color == Tile.P_White else Tile.P_White)
            return winner

    
    def check_terminal(self, board, color): 

        valid_moves = self.generate_all_possible_moves(board, color)
        return True if valid_moves == [] else False


    def opponent(self, tile):
        """
        Given a player symbol, returns the opponent's symbol, 'B' for black,
        or 'W' for white.  (3 - color)
        """
        return Tile.P_Black if tile == Tile.P_White else Tile.P_White


    def evaluate(self, board, color, terminal_value = 0):
        
        value = 0
        valid_moves_color = self.generate_all_possible_moves(board, color)
        valid_moves_opponent = self.generate_all_possible_moves(board, self.opponent(color))

        value += (10 * len(valid_moves_color))
        value -= (10 * len(valid_moves_opponent))

        value += terminal_value

        return value

