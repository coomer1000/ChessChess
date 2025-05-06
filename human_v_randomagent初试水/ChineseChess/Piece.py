
from ChineseChess.common import  full_name


class Piece:
    def __init__(self, player, en_name:str, point):
        self.player = player
        self.en_name = en_name
        self.full_name = full_name(en_name, player)
        self.point = point
    def __repr__(self):
        return f'name = {self.full_name},point = {self.point}'
