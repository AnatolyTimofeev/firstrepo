import random


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Board:
    def __init__(self, size=3):
        self.size = size
        self.field = [["."] * size for _ in range(size)]
        # self.x = []
        self.o = []

    def __str__(self):
        pole = ''
        pole += "  | 0 | 1 | 2 |"
        for i , j in enumerate(self.field):
            pole += f"\n{i} | " + " | ".join(j) + " |"
        return pole
    def moves(self, move , g = 'x'):
        self.g = g
        if g == 'x':

            while True:
                if self.field[move.x][move.y] == '.':
                    self.field[move.x][move.y] = g
                else:
                    print('Эта точка уже занята')
                    return False
                    break
                return self.field
        else:
            while True:
                if self.field[move.x][move.y] == '.' :
                    self.field[move.x][move.y] = g
                else:
                    if Board.standoff(self) != True:
                        # print('Компьютер ошибся')
                        return False
                        break
                    else:
                        break
                return self.field

    def win_(self,g):
        self.g = g
        y = self.field
        if [g, g, g] == y[0] or [g, g, g] == y[1] or [g, g, g] == y[2] \
                or y[0][0] == y[1][0] == y[2][0] == g or y[0][1] == y[1][1] == y[2][1] == g \
                or y[0][2] == y[1][2] == y[2][2] == g or y[0][0] == y[1][1] == y[2][2] == g \
                or y[0][2] == y[1][1] == y[2][0] == g:
            return True
    def standoff(self):
        s = []
        for i in range(3):
            for j in range(3):
                s.append(self.field[i][j])

        if '.' not in s:
            return True

class Player:

    def plmove(self):
         while True:

            self.y = input('Введите координату по горизонтали'  )
            self.x = input('Введите координату по вертикали'  )
            if not (self.x.isdigit()) or not (self.y.isdigit()):
                print('Введите числа')
                continue
            elif int(self.x) > 2 or int(self.x) < 0 or int(self.y) > 2 or int(self.y) < 0:
                 print('Введите число от 0 до 2')
                 continue
            else:
                return Dot(int(self.x)  , int(self.y))
                break

class Ai():
    def aimove(self):

        self.x = random.randrange(3)
        self.y = random.randrange(3)
        return Dot(self.x , self.y)

class Game:
    def __init__(self):
        self.ai = Ai()
        self.pl = Player()
        self.board = Board()

    def loop(self):
         while True:

            if self.board.win_('x') == True:
                 print('Вы победили')
                 break
            print(self.board)
            if self.board.win_('0') == True:
                 print('Компьютер победил')
                 break
            if self.board.standoff() == True:
                print('Ничья')
                break

            if self.board.moves(self.pl.plmove()) == False:
                continue
            print(self.board)

            while True:
                if self.board.moves(self.ai.aimove(), '0') == False:
                    continue
                else:
                    break
                    print(self.board)
                    print('Компьютер сходил')

a  = Game()
a.loop()



















