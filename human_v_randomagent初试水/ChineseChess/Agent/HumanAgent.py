from copy import deepcopy

from panel import interact

from ChineseChess.Game import GameState
from ChineseChess.Player import Player
from ChineseChess.ChessBoard import Board
from ChineseChess.Move import Move
from ChineseChess.Point import Point
from ChineseChess.common import FULL_FEN


class HumanAgent:
    def __init__(self, game):
        self.game = game
        self.board = self.game.board
        self.player = self.game.player

    def interact(self):
        """获取用户输入的起止坐标，并验证走法是否合法"""
        while True:  # 循环直到输入合法走法
            try:
                # 获取用户输入
                start = input('请输入起始坐标（格式：row,col）：')
                end = input("请输入目标坐标（格式：row,col）：")

                # 解析坐标
                start = Point(*map(int, start.split(',')))
                end = Point(*map(int, end.split(',')))

                # 获取棋子
                piece = self.board.get_piece(start)
                if not piece:
                    print(f"起始位置 {start} 没有棋子，请重新输入\n")
                    continue
                # 检查棋子是否属于当前玩家
                if piece.player != self.player:
                    print(f"这不是你的棋子，请选择{self.player}方的棋子\n")
                    continue
                move = Move(piece, start, end)
                valid_moves = self.game.is_valid_move(self.game.possible_moves())
                if move not in valid_moves:
                    print('不合法走子，请重新输入\n')
                    continue
                else:
                    print('合法')
                # 走法合法，执行移动
                self.board.move_piece(move)
                return move

            except ValueError as e:
                print(f"输入格式错误：{e}，请按正确格式输入（例如：2,3）\n")
            except Exception as e:
                print(f"发生错误：{e}，请重新输入\n")
if '__main__' == __name__:
    board = Board(fen = FULL_FEN, player = Player.Red)
    game = GameState(board)
    human = HumanAgent(game)
    print(human.interact())
    print(human.game.board._board)
