import matplotlib.pyplot as plt
import numpy as np
import pylab
from math import *
import math

# x = [1, 3, 7]
# x = np.array(x)
# y = x
# plt.title("Линейная зависимость y = x") # заголовок
# plt.xlabel("x") # ось абсцисс
# plt.ylabel("y") # ось ординат
# plt.grid()      # включение отображение сетки
# plt.plot(x, y)  # построение графика
# plt.show()
cort = []
x = []
y = []
t = []
s = []
alpha = []
c = 0
def ploting(fileName):
    print('Input multiplyer')
    mult = input()
    with open (fileName, 'r') as f:
        for line in f.readlines():
            cort.append(line)

        for i in range (len(cort)):
            x.append(int(cort[i].split(' ')[-3]))
            y.append(int(cort[i].split(' ')[-2]))
            t.append(int(cort[i].split(' ')[-1])/1000)

        for i in range (len(cort) - 1, -1, -1):
            x[i] = (x[i] - x[0])
            x[i] = x[i] * 0.33 / float(mult)
            y[i] = (y[i] - y[0])
            y[i] = y[i] * 0.33 / float(mult)


        plt.subplot(2, 2, 1)
        plt.plot(t, x)
        plt.xlabel('t, s')
        plt.ylabel('x, um')

        plt.subplot(2, 2, 3)
        plt.plot(t, y)
        plt.xlabel('t, s')
        plt.ylabel('y, um')

        s.append(0)
        alpha.append(0)
        for i in range (1, len(cort)):
            s.append(sqrt((x[i])**2 + (y[i])**2))
            if (sqrt((x[i])**2 + (y[i])**2) == 0):
                alpha.append(0)
            else:
                alpha.append(math.asin(y[i]/(sqrt((x[i])**2 + (y[i])**2))))
                s[i] = s[i] * np.sign(alpha[i])


        plt.subplot(1, 2, 2)
        plt.plot(t, s)
        plt.xlabel('t, s')
        plt.ylabel('s, um')
        plt.show()

if __name__ == "__main__":
    ploting('И26в.avi.result.txt')
