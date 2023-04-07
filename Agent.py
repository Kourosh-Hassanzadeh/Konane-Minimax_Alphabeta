from Tile import Tile

class Agent:

    MIN_VALUE = -1000000
    MAX_VALUE= 1000000

    def __init__(self, konane_game, color, max_depth):
        self.konane_game = konane_game
        self.color = color
        self.max_depth = max_depth
    

    def do_min_max(self, current_board):
        move, value = self.max(current_board, self.color, 0)
 
        return move
    

    def max(self, current_board, current_color, depth):
       
        if (self.konane_game.check_terminal(current_board, current_color)):
            return None, self.konane_game.evaluate(current_board, current_color, -1000)

        if (depth == self.max_depth):
            return None, self.konane_game.evaluate(current_board, current_color)

        possible_moves =  self.konane_game.generate_all_possible_moves(current_board, current_color)
        best_move = None
        best_move_value = self.MIN_VALUE
        for move in possible_moves:
            temp_move, value = self.min(current_board.next_board(current_color, move), self.konane_game.opponent(current_color), depth + 1, alpha, beta)
            if (value > best_move_value):
                best_move_value = value
                best_move = move
                
                # implement alpha-beta here
                
        return best_move, best_move_value

   
    def min(self, current_board, current_color, depth, alpha, beta):
        NotImplemented




