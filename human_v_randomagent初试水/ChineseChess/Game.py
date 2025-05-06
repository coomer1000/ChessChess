import copy

from ChineseChess.Player import Player
from ChineseChess.ChessBoard import Board
from ChineseChess.Move import Move
from ChineseChess.Point import Point
from ChineseChess.common import FULL_FEN, RED, BLACK, RESET
from ChineseChess.common import en_2_cn_dict

class GameState(object):
    '''
    功能:
    check_is_over, 检查是否缺少王
    is_checking, 下一步即将将军
    possible_moves, 己方棋手所有走法
    valid_moves, 合理走法
    '''
    def __init__(self, board,winner = None, is_checking = False):
        self.board = board
        self.player = self.board.player
        self.winner = winner
        self._is_checking = is_checking
        self.is_over = False
    def check_is_over(self):
        '''检查游戏是否结束'''
        all_pieces = self.board.get_all_piece()
        king_count = {'red': 0, 'black': 0}
        for piece in all_pieces:
            if piece.en_name == 'k':
                king_count['black'] += 1
            if piece.en_name == 'K':
                king_count['red'] += 1
        if king_count['red'] > king_count['black']:
            print(f'winner is red')
            self.is_over = True
        elif king_count['red'] < king_count['black']:
            print(f'winner is black')
            self.is_over = True
        else:
            self.is_over = False
    def is_checking(self, move):
        target_piece = self.board.get_piece(move.end_point)
        # 只有目标位置有棋子且是将/帅时才触发将军
        if target_piece and target_piece.en_name.lower() == 'k':
            print('下一步即将将军')
            self._is_checking = True
    def possible_moves(self):
        possible_moves = []
        for piece in self.board.get_all_piece():
            for i in range(10):
                for j in range(9):
                    if piece.point.row == i and piece.point.col == j:
                        continue
                    move = Move(piece, piece.point, Point(i, j))
                    possible_moves.append(move)
        return possible_moves
    def is_valid_move(self, possible_move):
        valid_moves = []
        for move in possible_move:
            piece = move.piece
            start_point, end_point = move.start_point, move.end_point
            start_piece = self.board.get_piece(start_point)
            end_piece = self.board.get_piece(end_point)
            # 1. 检查棋子是否属于当前玩家
            if piece.player != self.player:
                continue
            # 2. 检查目标位置是否是本方棋子
            if end_piece and end_piece.player == self.player:
                continue
            # 3. 根据棋子类型验证走法
            # 车（Rook）
            if piece.en_name.lower() == 'r':
                if not (start_point.row == end_point.row or start_point.col == end_point.col):
                    continue  # 车必须直线移动
                # 检查路径上是否有其他棋子
                if self._has_obstacle(start_point, end_point):
                    continue
            # TODO: 添加其他棋子（马、炮、兵等）的走法验证
            # 马（Knight)
            elif piece.en_name.lower() == 'n':  # 马（Horse）
                dx = abs(end_point.row - start_point.row)
                dy = abs(end_point.col - start_point.col)

                # 1. 检查是否是“日”字形移动
                if not ((dx == 2 and dy == 1) or (dx == 1 and dy == 2)):
                    continue  # 不是“日”字形
                # 2. 检查是否蹩马腿
                if dx == 2:  # 横向移动2格，纵向1格
                    # 马腿位置：横向中间点
                    middle_row = (start_point.row + end_point.row) // 2
                    if self.board.get_piece(Point(middle_row, start_point.col)):
                        continue  # 蹩马腿
                else:  # 纵向移动2格，横向1格
                    # 马腿位置：纵向中间点
                    middle_col = (start_point.col + end_point.col) // 2
                    if self.board.get_piece(Point(start_point.row, middle_col)):
                        continue  # 蹩马腿
            # 象/相（Bis
            elif piece.en_name.lower() == 'b':
                dx = abs(end_point.col - start_point.col)
                dy = abs(end_point.row - start_point.row)
                # 1. 田
                if not (dx == 2 and dy == 2):
                    continue

                # 2. 检查是否过河
                if (piece.player == Player.Red and end_point.row < 5) or \
                        (piece.player == Player.Black and end_point.row > 4):
                    continue

                # 3. 计算象眼位置（使用整数除法）
                middle_row = (start_point.row + end_point.row) // 2
                middle_col = (start_point.col + end_point.col) // 2
                # 4. 检查象眼是否被堵
                if self.board.get_piece(Point(middle_row, middle_col)):
                    continue
            # 士/仕（A
            elif piece.en_name.lower() == 'a':
                dx = abs(end_point.col - start_point.col)
                dy = abs(end_point.row - start_point.row)
                # 1. 斜一
                if not (dx == 1 and dy == 1):
                    continue
                # 2. 检查是否在九宫格内
                if piece.player == Player.Red:  # 红方仕
                    if not (7 <= end_point.row <= 9 and 3 <= end_point.col <= 5):
                        continue
                else:  # 黑方士
                    if not (0 <= end_point.row <= 2 and 3 <= end_point.col <= 5):
                        continue
            # 将/帅（King）
            elif piece.en_name.lower() == 'k':
                dx = abs(end_point.col - start_point.col)
                dy = abs(end_point.row - start_point.row)
                if dx + dy != 1:
                    continue
                # 检查是否在九宫格内
                if piece.player == Player.Red:  # 红
                    if not (7 <= end_point.row <= 9 and 3 <= end_point.col <= 5):
                        continue
                else:  # 黑
                    if not (0 <= end_point.row <= 2 and 3 <= end_point.col <= 5):
                        continue
            # 炮（Cannon）
            elif piece.en_name.lower() == 'c':
                # 1. 检查是否是直线移动
                if not (start_point.row == end_point.row or start_point.col == end_point.col):
                    continue
                # 2. 统计起点和终点之间的棋子数
                obstacle_count = self._count_obstacles(start_point, end_point)
                # 3. 判断是移动还是吃子
                if end_piece:  # 目标位置有棋子（吃子）
                    if obstacle_count != 1:  # 必须正好有一个炮架
                        continue
                else:  # 目标位置无棋子（移动）
                    if obstacle_count != 0:  # 路径上不能有棋子
                        continue
            # 兵/卒(P
            elif piece.en_name.lower() == 'p':  # 兵/卒
                dx = end_point.col - start_point.col  # 横向变化
                dy = end_point.row - start_point.row  # 纵向变化
                # 确保每次只移动一格
                if abs(dx) + abs(dy) != 1:
                    continue
                # 红方兵
                if piece.player == Player.Red:
                    # 未过河
                    if start_point.row >=5:
                        if dy != -1:  # 只能向下(行数增加)
                            continue
                    # 已过河
                    else:
                        if dy != -1 and abs(dx) != 1:  # 可以向下或左右
                            continue

                # 黑方卒
                else:
                    # 未过河
                    if start_point.row <=4:
                        if dy != 1:  # 只能向上(行数减少)
                            continue
                    # 已过河
                    else:
                        if dy != 1 and abs(dx) != 1:  # 可以向上或左右
                            continue
            valid_moves.append(move)  # 通过所有检查的走法
        return valid_moves
    def _has_obstacle(self, start, end):
        """检查两点之间是否有障碍物（用于车，炮）"""
        if start.row == end.row:  # 横向移动
            step = 1 if end.col > start.col else -1
            for col in range(start.col + step, end.col, step):
                if self.board.get_piece(Point(start.row, col)):
                    #print('有阻挡的棋子')
                    return True
        elif start.col == end.col:  # 纵向移动
            step = 1 if end.row > start.row else -1
            for row in range(start.row + step, end.row, step):
                if self.board.get_piece(Point(row, start.col)):
                    return True
        return False
    def _count_obstacles(self, start, end):
        """计算两点之间的棋子数量"""
        count = 0
        if start.row == end.row:  # 横向移动
            step = 1 if end.col > start.col else -1
            for col in range(start.col + step, end.col, step):
                if self.board.get_piece(Point(start.row, col)):
                    count += 1
        elif start.col == end.col:  # 纵向移动
            step = 1 if end.row > start.row else -1
            for row in range(start.row + step, end.row, step):
                if self.board.get_piece(Point(row, start.col)):
                    count += 1
        return count
    def apply_move(self, move):
        print(move)
        new_board = copy.deepcopy(self.board)
        new_board.move_piece(move)
        new_board.player = Player.playerchange(self.board.player)
        new_game = GameState(new_board)
        new_game.check_is_over()
        #print(new_board._board)
        return new_game
    def print_board(self):
        for row in self.board._board:
            for piece in row:
                if piece.isupper():
                    print(f"{RED}{en_2_cn_dict(piece)}{RESET}", end=" ")  # 红方棋子
                elif piece.islower():
                    print(f"{BLACK}{en_2_cn_dict(piece)}{RESET}", end=" ")  # 黑方棋子（默认黑色）
                else:
                    print("口", end=" ")  # 空格
            print()

if __name__ == '__main__':
    game = GameState(board = Board(fen = FULL_FEN, player = Player.Red))
    for i in game.is_valid_move(game.possible_moves()):
        if i.piece.en_name.lower() == 'a':
            print(i,end='\n')




