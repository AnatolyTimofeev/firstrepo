from random import randint

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y # переопределяем сравнивание координат через их значения
    
    def __repr__(self):
        return f"({self.x}, {self.y})" # для того чтобы координаты возвращались в виде кортежа (x,y)


class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow                     # bow - координаты носа коробля в виде кортежа(x,y) , длина, ориентация
        self.l = l                         # o=0 корабль расположен по оси x , o=1 по оси y
        self.o = o
        self.lives = l
    
    @property
    def dots(self):
        ship_dots = []                    # список в котором хранятся координаты короблей
        for i in range(self.l):
            cur_x = self.bow.x 
            cur_y = self.bow.y
            
            if self.o == 0:
                cur_x += i
            
            elif self.o == 1:
                cur_y += i
            
            ship_dots.append(Dot(cur_x, cur_y))
        
        return ship_dots
    
    def shooten(self, shot):                        # проверяет наличие точки в списке кораблей
        return shot in self.dots

class Board:
    def __init__(self, hid = False, size = 6):      # переменная hid для скрытия поля компьютера/игрока
        self.size = size
        self.hid = hid
        
        self.count = 0                                  # количество пораженных кораблей
        
        self.field = [ ["O"]*size for _ in range(size) ]
        
        self.busy = []                                  # точки занятые короблем либо в которые уже стреляли
        self.ships = []                                 # список кораблей доски
    
    def add_ship(self, ship):
        
        for d in ship.dots:
            if self.out(d) or d in self.busy:            # если точка вне поля или ячека уже занята то исключение
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb = False):
        near = [                                # список точек вокруг коробля
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for d in ship.dots:                     # происходит смещение по длине коробля и добавляются точки вокруг коробля
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:                                     # False в начале игры
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)
    
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"
        
        if self.hid:                                         # если hid=True то заменяем квадратики на нолики
            res = res.replace("■", "O")
        return res
    
    def out(self, d):                                              # проверяет что точка не выходит за пределы доски
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

    def shot(self, d):                                            # метод выстрел
        if self.out(d):
            raise BoardOutException()                             # если за пределами доски то исключение
        
        if d in self.busy:
            raise BoardUsedException()                            # если точка занята то исключение
        
        self.busy.append(d)
        
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1                       # количество жизней коробля
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        
        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False
    
    def begin(self):
        self.busy = []

class Player:                                              # передается две доски
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    
    def ask(self):
        raise NotImplementedError()                        # будет наследоваться в класс игрока и компьютера и вызывать исключение
    
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):                                      #наследуется от Player
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")       # случайная генерация 2 точек
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            
            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue
            
            x, y = cords
            
            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue
            
            x, y = int(x), int(y)
            
            return Dot(x-1, y-1)

class Game:
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        
        self.ai = AI(co, pl)
        self.us = User(pl, co)
    
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board
    
    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]            # длина и количество короблей
        board = Board(size = self.size)
        attempts = 0
        for l in lens:                          # будет случайным образом расставлять коробли пока количество
            while True:                         # меньше 2000
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):                              # приветствие
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
    
    
    def loop(self):
        num = 0                                # счетчик ходов
        while True:
            print("-"*20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-"*20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:                 # если четный то ход пользователя
                print("-"*20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-"*20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.count == 7:         # количество уничтоженных кораблей
                print("-"*20)
                print("Пользователь выиграл!")
                break
            
            if self.us.board.count == 7:
                print("-"*20)
                print("Компьютер выиграл!")
                break
            num += 1
            
    def start(self):
        self.greet()
        self.loop()
            
            
g = Game()
g.start()