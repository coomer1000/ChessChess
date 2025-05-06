
class Move:
    def __init__(self, piece, start_point, end_point, is_checking=False):
        self.piece = piece
        self.start_point = start_point
        self.end_point = end_point
        self.is_checking = is_checking
    def __repr__(self):
        return f'{self.piece.full_name} : from {self.start_point} to {self.end_point}'

    def __eq__(self, other):
        if (self.piece == other.piece
            and self.start_point == other.start_point
            and self.end_point == other.end_point):
            return True

