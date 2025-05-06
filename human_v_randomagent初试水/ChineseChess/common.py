
import numpy as np


FULL_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR'
RED = "\033[31m"
BLACK = "\033[32m"
RESET = "\033[0m"
def fen_2_board(fen):
    rows = fen.split('/')
    board = np.array([['-' for i in range(9)] for j in range(10)])
    i = -1
    for row in rows:
        i += 1
        j = -1
        for ch in row:
            if ch.isdigit():
                j += int(ch)
            else:
                j += 1
                board[i][j] = ch
    return board
def en_2_cn_dict(en):
    _en_2_cn_dict = {
        'r':'车', 'R':'车', 'n':'马', 'N':'马', 'b':'象', 'B':'相', 'a':'士', 'A':'仕',
        'k':'将', 'K':'帅' ,'c':'炮', 'C':'炮', 'p':'卒', 'P':'兵'
    }
    return _en_2_cn_dict.get(en)
def full_name(en, player):
    full_name = player.value + en_2_cn_dict(en)
    return full_name
