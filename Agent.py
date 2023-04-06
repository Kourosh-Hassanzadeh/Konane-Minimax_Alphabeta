from Tile import Tile


class Agent:

    MIN_VALUE = -1000000
    MAX_VALUE= 1000000

    def __init__(self, board, max_depth):
        self.board = board
        self.max_depth = max_depth

    def do_min_max(self, current_board, current_color):
        # For alpha-beta pruning: add 2 more arguments ->   self.MIN_VALUE, self.MAX_VALUE
        move, value = self.max(current_board, current_color, 0)
 
        return move
    
    # For alpha-beta pruning: add 2 more parameters ->  alpha, beta
    def max(self, current_board, current_color, depth):
       
        if (self.check_terminal(current_board, current_color)):
            return None, self.evaluate(current_board, current_color, -1000)

        if (depth == self.max_depth):
            return None, self.evaluate(current_board, current_color)

        possible_moves = self.create_possible_moves(current_board, current_color)
        best_move = None
        best_move_value = self.MIN_VALUE
        for move in possible_moves:
            temp_move, value = self.min(self.board.next_board(current_board, current_color, move),  self.board.opponent(current_color), depth + 1, alpha, beta)
            if (value > best_move_value):
                best_move_value = value
                best_move = move

            # implement alpha-beta here
                
        return best_move, best_move_value

   
    def min(self, current_board, current_color, depth):
        NotImplemented


    def evaluate(self, board, color, terminal_value = 0):
        
        value = 0
        valid_moves_color = self.create_possible_moves(board, color)
        valid_moves_opponent = self.create_possible_moves(board, self.board.opponent(color))

        value += (10 * len(valid_moves_color))
        value -= (10 * len(valid_moves_opponent))

        value += terminal_value

        return value


    def check_terminal(self, board, color): 

        valid_moves = self.create_possible_moves(board, color)
        return True if valid_moves == [] else False


    def create_possible_moves(self, board, color):
        return self.board.generate_all_possible_moves(board, color)
