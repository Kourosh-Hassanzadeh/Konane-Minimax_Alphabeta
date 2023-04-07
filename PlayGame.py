from PlayKonane import PlayKonane
from Tile import Tile
from Agent import Agent
from Board import Board
from KonaneGame import KonaneGame


class PlayGame:

    def __init__(self):
        NotImplemented

    def play(self):
        size = 6
        konane_game = KonaneGame()
        initial_board = Board(size, konane_game.initialize_board(size))
        agent1 = Agent(konane_game, color=Tile.P_Black, max_depth=4)
        agent2 = Agent(konane_game, color=Tile.P_White, max_depth=2)
        # bot vs bot
        game = PlayKonane(initial_board, konane_game, agent1=agent1, agent2=agent2)

        # player vs bot
        #game = PlayKonane(initial_board, konane_game, agent1=agent2)
    



if __name__ == '__main__':
    PlayGame().play()