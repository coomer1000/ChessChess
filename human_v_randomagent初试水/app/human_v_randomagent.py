from ChineseChess.Game import GameState
from ChineseChess.Player import Player
from ChineseChess.Agent.HumanAgent import HumanAgent
from ChineseChess.Agent.RandomAgent import RandomAgent
from ChineseChess.ChessBoard import Board
from ChineseChess.common import FULL_FEN

def main():
    board = Board(fen = FULL_FEN, player = Player.Red)
    game = GameState(board)
    player1 = HumanAgent(game) # player1 为红方
    player2 = RandomAgent(game) # player2 为黑方
    # players = {
    #     Player.Red: player1,
    #     Player.Black: player2
    # }
    # 开始对弈
    while not game.is_over:
        print(f'现在是{game.player.value}方的回合')
        if game.player == Player.Red:
            move = player1.interact()
            game = game.apply_move(move)
            game.print_board()
        else:
            move = player2.select_move(game)
            game = game.apply_move(move)
            game.print_board()

        if game.is_over:
            break
if __name__ == '__main__':
    main()

