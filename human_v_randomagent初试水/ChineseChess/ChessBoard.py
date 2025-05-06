from copy import deepcopy

from ChineseChess.Move import Move
from ChineseChess.Piece import Piece
from ChineseChess.Point import Point
from ChineseChess.common import fen_2_board, FULL_FEN
from ChineseChess.Player import Player

class Board:
    '''
    功能：
    get_piece，获取全部棋子
    move_piece，移动棋子，更新_board和 piece_point_dict
    属性：
    init_fen，由此生成_board
    player, 存储玩家
    _board,存储棋盘 10row * 9col
    piece_point_dict, 将point和 piece对应起来
    '''
    def __init__(self, fen, player):
        self.init_fen = fen
        self._board = fen_2_board(fen)
        self.piece_point_dict = self.create_piece_point_dict_from_board()
        self.player = player
    def create_piece_point_dict_from_board(self):
        piece_point_dict = {}
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j] != '-':
                    player = Player.Red if self._board[i][j].isupper() else Player.Black
                    piece = Piece(player, self._board[i][j], Point(i, j))
                    piece_point_dict[Point(i, j)] = piece
                else:
                    continue
        return piece_point_dict
    def get_piece(self, point):
        return self.piece_point_dict.get(point)
    def get_all_piece(self):
        return self.piece_point_dict.values()
    def move_piece(self, move):
        start_point = move.start_point
        end_point = move.end_point
        piece = self.get_piece(start_point)
        if not piece:
            return False
        #更新piece_point_dict的Point()和piece
        self.piece_point_dict[end_point] = piece
        self.piece_point_dict[end_point].point = end_point
        del self.piece_point_dict[start_point]
        #更新_board
        old_row, old_col = start_point.row, start_point.col
        new_row, new_col = end_point.row, end_point.col
        self._board[new_row][new_col] = piece.en_name
        self._board[old_row][old_col] = '-'
        return True

if __name__ == '__main__':
    board = Board(fen = FULL_FEN, player = Player.Red)
    point = Point(9, 0)
    piece = board.get_all_piece(point)
    print(f'玩家{board.player}下棋ing')
    print('选择棋子：\n',board.get_piece(point))
    move = Move(piece,start_point=piece.point,end_point = Point(9,1))
    board.move_piece(move)
    print('移动变化:\n',move)
    print('棋盘如下:\n',board._board)
    print(f'现在为玩家{board.player}')
