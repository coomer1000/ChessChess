import random
from ChineseChess.Game import GameState

class RandomAgent:
    def __init__(self, game):
        self.game = game
        self.player = self.game.player
        self.board = game.board
    def select_move(self, game):
        rnd_move = None
        moves_ls = game.is_valid_move(game.possible_moves())
        for move in moves_ls:
            game.is_checking(move)
            if game._is_checking == True:
                rnd_move = move
                break
            else:
                rnd_move = random.choice(moves_ls)
        return rnd_move
    def non_agressive_state(self, board):
        pass