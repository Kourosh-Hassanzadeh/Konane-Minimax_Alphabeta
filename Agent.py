from Tile import Tile

class Agent:

    MIN_VALUE = -1000000
    MAX_VALUE= 1000000

    def __init__(self, game_manager, color, max_depth):
        self.game_manager = game_manager
        self.color = color
        self.max_depth = max_depth
    

    def do_min_max(self, current_board):
        # For alpha-beta pruning: add 2 more arguments ->   self.MIN_VALUE, self.MAX_VALUE
        move, value = self.max(current_board, self.color, 0)
 
        return move
    
    # For alpha-beta pruning: add 2 more parameters ->  alpha, beta
    def max(self, current_board, current_color, depth):
       
        if (self.game_manager.check_terminal(current_board, current_color)):
            return None, self.game_manager.evaluate(current_board, current_color, -1000)

        if (depth == self.max_depth):
            return None, self.game_manager.evaluate(current_board, current_color)

        possible_moves =  self.game_manager.generate_all_possible_moves(current_board, current_color)
        best_move = None
        best_move_value = self.MIN_VALUE
        for move in possible_moves:
            temp_move, value = self.min(self.game_manager.next_move(current_board, current_color, move), self.game_manager.opponent(current_color), depth + 1, alpha, beta)
            if (value > best_move_value):
                best_move_value = value
                best_move = move
                
                # implement alpha-beta here
                
        return best_move, best_move_value

   
    def min(self, current_board, current_color, depth, alpha, beta):
        NotImplemented




