from PlayKonane import PlayKonane
from Tile import Tile
from Agent import Agent
from Board import Board
from KonaneGameManager import GameManager


class KonaneGame:

    def __init__(self):
        NotImplemented

    def play(self):
        size = 6
        initial_board = Board(size, self.initialize_board(size))
        game_manager = GameManager()
        agent1 = Agent(game_manager, color=Tile.P_Black, max_depth=4)
        agent2 = Agent(game_manager, color=Tile.P_White, max_depth=2)
        # bot vs bot
        game = PlayKonane(initial_board, game_manager, agent1=agent1, agent2=agent2)

        # player vs bot
        #game = PlayKonane(initial_board, agent1=agent1)
    

    def initialize_board(self, board_size):
        board = []
        tile = Tile(2,0,0,0)
        for i in range(board_size):
            row_gui = []
            for j in range(board_size):
                row_gui.append(tile)
                tile = Tile(3-tile.piece, tile.outline, i, j+1)
            board.append(row_gui)
            if board_size%2 == 0:
                tile = Tile(3-tile.piece, tile.outline, i+1, 0)

        return board


if __name__ == '__main__':
    KonaneGame().play()