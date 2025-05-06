from collections import namedtuple

#内存存储位置不同则认为不同，而namedtuple可直接解决。
class Point(namedtuple('Point','x,y')):
    '''位置类'''
    @property
    def row(self):
        return self.x
    @property
    def col(self):
        return self.y
    def __repr__(self):
        return f'Point(row={self.x},col={self.y})'
