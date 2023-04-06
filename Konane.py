import random
from GUInterface import Graphic
from Tile import Tile
from Board import Board
from Agent import Agent


class Konane:

    def __init__(self, n, pve = True):
        self.size = n
        self.initialize_game(pve)
        
    def initialize_game(self, pve):
        """
        Resets the starting board state.
        """
        self.computing = False
        self.selected_tile = None
        self.current_player = Tile.P_Black
        self.valid_moves = []
        self.board = Board(self.size)
        self.game_board = self.board.initialize_board()
        self.c_player=Tile.P_White
        self.agent = Agent(self.board, 4)
        self.board_view = Graphic(self.game_board)
        self.game_finished = False

        if pve:
            self.board_view.add_click_handler(self.tile_clicked)
        else:
            self.agent2 = Agent(self.board, 2)
            self.run_bot_vs_bot()

        #GUI settings        
        self.board_view.draw_tiles(board = self.game_board)
        self.board_view.mainloop()


    def run_bot_vs_bot(self):

        self.execute_computer_move(self.agent)
        if not self.game_finished:
            self.execute_computer_move(self.agent2)
        if not self.game_finished:
            self.run_bot_vs_bot()



    def tile_clicked(self, row, col):
  
        if self.computing:  # Block clicks while computing
            return
        new_tile = self.game_board[row][col]
        # If we are selecting a friendly piece

        if self.board.opening_move(self.game_board):
            self.selected_tile = new_tile
            self.valid_moves = self.get_moves_at_tile(new_tile, self.current_player)
            for tile in  self.valid_moves:
                if self.selected_tile == tile:
                    self.outline_tiles(None)  # Reset outlines
                    self.do_move(self.current_player, [self.selected_tile.row, self.selected_tile.col, new_tile.row, new_tile.col])

                    # Update status and reset tracking variables
                    self.selected_tile = None
                    self.valid_moves = []
                    self.toggle_current_player()
                    if self.c_player is not None:
                        self.execute_computer_move(self.agent)


        elif new_tile.piece == self.current_player:
            
            self.outline_tiles(None)  # Reset outlines
            
            # Outline the new and valid move tiles
            new_tile.outline = Tile.O_MOVED
            self.valid_moves = self.get_moves_at_tile(new_tile, self.current_player)
            
            # Update status and save the new tile
            self.outline_tiles(self.valid_moves)
            self.board_view.set_status("Tile `" + str(new_tile.row) + "," + str(new_tile.col) +"` selected")
            self.selected_tile = new_tile

            self.board_view.draw_tiles(board = self.game_board)  # Refresh the board

        # If we already had a piece selected and we are moving a piece
        elif self.selected_tile and new_tile in self.valid_moves:
            self.outline_tiles(None)  # Reset outlines
            self.do_move(self.current_player, [self.selected_tile.row, self.selected_tile.col, new_tile.row, new_tile.col])

            # Update status and reset tracking variables
            self.selected_tile = None
            self.valid_moves = []
            self.toggle_current_player()
         
            # If there is a winner to the game
            winner = self.find_winner(self.current_player)
            if winner:
                self.board_view.set_status("The " + ("white"
                    if winner == Tile.P_White else "black") + " player has won!")
                self.current_player = None
                self.print_winner(winner)
                print(self.boardToStr(self.game_board))
            
            elif self.c_player is not None:
                self.execute_computer_move(self.agent)
            
        else:
            self.board_view.set_status("Invalid move attempted")    


    def get_moves_at_tile(self, tile, player):
        moves =  self.board.generate_all_possible_moves(self.game_board, player)
        valid_moves_at_tile = []
        print(moves)
        for move in moves:
            if move[0] == tile.row and move[1] == tile.col:
                valid_tile = self.game_board[move[2]][move[3]]
                valid_moves_at_tile.append(valid_tile)
        return valid_moves_at_tile
    

    def do_move(self, player, move):
        """
        Updates the current board with the next board created by the given
        move.
        """
        self.computing = True
        self.game_board = self.board.next_board(self.game_board, player, move)
       # self.print_result()
        self.board_view.draw_tiles(board = self.game_board)
        self.computing = False
        print("player: " + str(player))
        print(self.boardToStr(self.game_board))
        print("---------------------------")


    def outline_tiles(self, tiles=[], outline_type=Tile.O_SELECT):

        if tiles is None:
            tiles = [j for i in self.game_board for j in i]
            outline_type = Tile.O_NONE

        for tile in tiles:
            tile.outline = outline_type   


    def find_winner(self, color):
        valid_moves = self.board.generate_all_possible_moves(self.game_board, color)

        if valid_moves == []:
            winner = (Tile.P_Black if color == Tile.P_White else Tile.P_White)
            return winner


    def execute_computer_move(self, agent):

        self.computing = True
        self.board_view.update()
        max_depth = 3

        move = agent.do_min_max(self.game_board, self.current_player)

        self.outline_tiles(None)  # Reset outlines

        self.do_move(self.current_player, move)

        self.toggle_current_player()
        winner = self.find_winner(self.current_player)
        if winner:
            self.board_view.set_status("The " + ("white"
                if winner == Tile.P_White else "black") + " player has won!")
            self.board_view.set_status_color("#212121")
            self.current_player = None
            self.print_winner(winner)
            self.game_finished = True

        self.computing = False
        
        print()

    def print_winner(self, winner):
        print()
        print("Final Stats")
        print("===========")
        print("Final winner:", "white"
            if winner == Tile.P_White else "black")


    def toggle_current_player(self):
        self.current_player = (Tile.P_Black
                if self.current_player == Tile.P_White else Tile.P_White)



    def boardToStr(self, board):
            """
            Returns a string representation of the konane board.
            """
            result = "  "
            for i in range(self.size):
                result += str(i) + " "
            result += "\n"
            for i in range(self.size):
                result += str(i) + " "
                for j in range(self.size):
                    result += str(board[i][j].piece) + " "
                result += "\n"
            return result


if __name__ == '__main__':
    # pve : True = player vs bot    False = bot vs bot
    # 6 = board size 6x6
    game = Konane(6, pve = True)
   