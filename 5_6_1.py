import random
z=q=0
str_y=''
y = [['.','.','.'],
     ['.','.','.'],
     ['.','.','.']]
def s():
    str_y = f"""   0 1 2 \n 0 {y[0][0]} {y[0][1]} {y[0][2]}\n 1 {y[1][0]} {y[1][1]} {y[1][2]}\n 2 {y[2][0]} {y[2][1]} {y[2][2]}"""
    print(str_y)

def win_(i):
         if [i,i,i] == y[0] or [i,i,i] == y[1] or [i,i,i] == y[2] \
                 or y[0][0]==y[1][0]==y[2][0]==i or y[0][1]==y[1][1]==y[2][1] == i\
                 or y[0][2]==y[1][2]==y[2][2] == i or y[0][0]==y[1][1]==y[2][2] == i\
                 or y[0][2]==y[1][1]==y[2][0] == i:
             return True

s()
while '.' not in y:
    q = input('Ваш ход. Введите координатy  x по горизонтали :  ')
    z = input('Введите координату x по вертикали : ')
    if not(q.isdigit()) or not (z.isdigit):
        print('Введите числа')
        continue
    else:
        q = int(q)
        z = int(z)
    if  q > 2 or q < 0 or z > 2 or z < 0:
        print('Введите число от 0 до 2')
        continue
    if y[z][q] == '.':
        y[z][q]  ='x'

    else:
        print('Это поле уже занято')
        continue
    if win_('x'):
        print('Вы победили !')
        s()
        break
    while y[z][q] == 'x' or y[z][q] == '0' :
        q = random.randrange(len(y))
        z = random.randrange(len(y))
      #  print(q,z)
        if y[z][q] == '.':
            y[z][q] = '0'

            print('Компьютер сходил')
            s()
            break
    if win_('0'):
        print('Вы проиграли !')
                           
        break

