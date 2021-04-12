import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

# Входные данные
x_arr = [1, 1.2, 1.4, 1.6, 1.8, 2]
y_arr = [15, 16, 17, 18, 19, 20]

matr = [(2, 1, 0, 0, 0, 0),
        (2, 2, 1, 0, 0, 0),
        (0, 2, 10, 0, 0, 0),
        (0, 1, 3, 2, 0, 0),
        (0, 0, 2, 2, 1, 0),
        (0, 0, 0, 0, 2, 3)]
nx_arr = [4, 6, 16, 4, 3, 3]
ny_arr = [3, 5, 12, 6, 5, 5]

# 1. Построить корреляционное поле.

# Вычислим числовые хар-ки
x_average = sum(x_arr) / len(x_arr)
y_average = sum(y_arr) / len(y_arr)

s2x = 0
s2y = 0
for i in range(len(x_arr)):
    s2x += (x_arr[i] - x_average) ** 2
    s2y += (y_arr[i] - y_average) ** 2
s2x /= len(x_arr) - 1
s2y /= len(y_arr) - 1
sx = math.sqrt(s2x)
sy = math.sqrt(s2y)

xy_average = 0
for i in range(len(x_arr)):
    xy_average += x_arr[i] * y_arr[i]
xy_average /= len(x_arr)

# Определим значимость коэф. корреляции
r = round((xy_average - x_average * y_average) / (sx * sy), 3)      # коэф линейной корреляции

# Напишем эмпирическое уравнение линий регрессий
print("уравнения регрессий: ")
y_reg = complex(round(y_average - x_average * r * sy / sx, 5), round(r * sy / sx, 5))
x_reg = complex(round(x_average - y_average * r * sx / sy, 5), round(r * sx / sy, 5))
print("y^x = ", y_reg)
print("x^y = ", x_reg)

# Линейные регрессии
yx_arr = []
xy_arr = []
for i in range(len(x_arr)):
    yx_arr.append(round(y_reg.real + y_reg.imag * x_arr[i], 4))
    xy_arr.append(round(x_reg.real + x_reg.imag * y_arr[i], 4))

plt.plot(x_arr, y_arr, 'ro', color="gray", label="Результаты наблюдений")
plt.plot(x_arr, yx_arr, color="blue", label="Линейная регрессия x на y")
plt.plot(xy_arr, y_arr, color="red", label="Линейная регрессия y на x")
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Координатная плоскость')
plt.legend()
plt.grid()      # включение отображение сетки
plt.show()

# По характеру расположения точек в корреляционном поле выбрать общий вид регрессии.

yxj_arr = []

for j in range(len(nx_arr)):
    sum = 0
    for i in range(len(ny_arr)):
        sum += matr[i][j] * y_arr[i]
    yxj_arr.append(round(sum/nx_arr[j],3))
# print(yxj_arr)

plt.plot(x_arr ,yxj_arr, 'ro')
plt.grid()
plt.show()

# 2. Написать уравнение линии регрессии y на x по методу наименьших квадратов и с использованием коэффициента корреляции r.
# Сравнить полученные уравнения и сделать вывод о выборе одного из них.
nxx_arr = []
nxx2_arr = []
n = np.sum(nx_arr) #самому смешно
nyy_arr = [] #нейминг просто бомба честно говоря
nxyxy_arr = []


for i in range(len(nx_arr)):
    perem = 0
    nxx_arr.append(round((nx_arr[i]*x_arr[i]), 2))
    nxx2_arr.append(round((nx_arr[i]*(x_arr[i]**2)), 2))
    nyy_arr.append(ny_arr[i]*y_arr[i])
    for j in range(len(ny_arr)):
        perem += matr[j][i] * y_arr[j]
    nxyxy_arr.append(perem * x_arr[i])
print(nxx_arr, nxx2_arr, nyy_arr, nxyxy_arr)

M1 = np.array([[n, np.sum(nxx_arr)], [np.sum(nxx_arr), np.sum(nxx2_arr)]]) #левая часть системы
v1 = np.array([np.sum(nyy_arr), np.sum(nxyxy_arr)]) #правая часть системы
# print(M1, v1) # Проверяем систему (гуд)
_Yx = np.linalg.solve(M1, v1)
print("Решение СЛАУ:", np.linalg.solve(M1, v1))


# 14 слайд n>30 then
C1_mox = max(x_arr)
C2_moy = max(y_arr)
h1 = x_arr[1] - x_arr[0]
h2 = y_arr[1] - y_arr[0]

for i in range(len(x_arr)):
    if nx_arr == C1_mox:
        C1_mox = x_arr[i]
        break
for i in range(len(y_arr)):
    if ny_arr == C2_moy:
        C2_moy = y_arr[i]
        break
# print(C1_mox,C2_moy)

ui = []
vj = []
for i in range(len(x_arr)):
    ui.append((x_arr[i] - C1_mox) / h1)
    vj.append((y_arr[i] - C2_moy) / h2)
print(ui, vj)

# 16 слайд
OneDivN = 1 / n
_U = 0
_V = 0
_U2 = 0
_V2 = 0
for i in range(len(ui)):
    _U += nx_arr[i] * ui[i]
    _V += ny_arr[i] * vj[i]
    _U2 += nx_arr[i] * ui[i]**2
    _V2 += ny_arr[i] * vj[i]**2
_U *= OneDivN
_U2 *= OneDivN
_V *= OneDivN
_V2 *= OneDivN
print(_U,_V,_U2,_V2)

Su = math.sqrt(_U2 - _U**2)
Sv = math.sqrt(_V2 - _V**2)
# print(Su,Sv)

# Таблица 30
indexX0 = 0
indexY0 = 0

for i in range(len(nx_arr)):
    if ui[i] == 0:
        indexX0 = i
        break
for i in range(len(ny_arr)):
    if vj[i] == 0:
        indexY0 = i
        break

table30up = np.empty((len(x_arr), len(ny_arr)), dtype = "float64")
for i in range(len(ny_arr)):
    table30up[i, indexX0] = 0
for i in range(len(nx_arr)):
    table30up[indexY0, i] = 0
tab30down = np.empty((len(x_arr), len(ny_arr)), dtype = "float64")
for i in range(len(ny_arr)):
    for j in range(len(nx_arr)):
        if table30up[i, j] != 0:
            tab30down[i, j] = vj[i] * ui[j]
tab30right = np.empty((len(x_arr)), dtype="float64")
for i in range(len(ny_arr)):
    for j in range(len(nx_arr)):
        tab30right[i] += table30up[i, j] * tab30down[i, j]

tableSum = np.sum(tab30right)
# print(tableSum)

# 19 Слайд
rv = (tableSum - n * _U * _V) / (n * Su * Sv)

_x = _U * h1 + C1_mox
_y = _V * h2 + C2_moy

Sx = Su * h1
Sy = Sv * h2
print(f"Rv = {round(rv,2)}; _x = {round(_x,2)}; _y = {round(_y,2)}; Sx = {round(Sx,2)}; Sy = {round(Sy,2)};")

# 3. Оценить тесноту связи между признаками X и Y с помощью выборочного коэффициента корреляции r и его значимость.
th = (math.fabs(rv) * math.sqrt(n - 2))
th /= math.sqrt(1 - rv**2) #"""Ошибка"""
print(th)

tak = 2.0423
#TODO 418 строка 21 слайд

# 4. Проверить адекватность модельного уравнения регрессии y на x, записанного через коэффициент корреляции r.

# 5. Проверить надежность уравнения регрессии y на x, записанного через коэффициент корреляции r и его коэффициентов.

# 6. Построить уравнения регрессий в первоначальной системе координат.
