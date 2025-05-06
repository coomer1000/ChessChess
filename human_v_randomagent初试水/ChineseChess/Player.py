from enum import Enum
class Player(Enum):
    Red = '红'
    Black = '黑'
    @classmethod
    #关于为什么要用到类方法，如果 playerchange() 是实例方法，它应该返回新玩家对象而非修改自身。
    def playerchange(cls, player):
        if player == cls.Red:
            return cls.Black
        elif player == cls.Black:
            return cls.Red
if __name__ == '__main__':
    player = Player.Black
    print(player)

