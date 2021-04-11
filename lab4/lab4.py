import matplotlib.pyplot as plt
import seaborn as sns
import math

x_arr = [1, 1.2, 1.4, 1.6, 1.8, 2]
y_arr = [15, 16, 17, 18, 19, 20]

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
matr = [(2, 1, 0, 0, 0, 0),
        (2, 2, 1, 0, 0, 0),
        (0, 2, 10, 0, 0, 0),
        (0, 1, 3, 2, 0, 0),
        (0, 0, 2, 2, 1, 0),
        (0, 0, 0, 0, 2, 3)]
nx_arr = [4, 6, 16, 4, 3, 3]
ny_arr = [3, 5, 12, 6, 5, 5]

yxj_arr = []

for j in range(len(nx_arr)):
    sum = 0
    for i in range(len(ny_arr)):
        sum += matr[i][j] * y_arr[i]
    yxj_arr.append(round(sum/nx_arr[j],3))
print(yxj_arr)

plt.plot(x_arr ,yxj_arr, 'ro')
plt.grid()
plt.show()

# 2. Написать уравнение линии регрессии y на x по методу наименьших квадратов и с использованием коэффициента корреляции r.
# Сравнить полученные уравнения и сделать вывод о выборе одного из них.

# 3. Оценить тесноту связи между признаками X и Y с помощью выборочного коэффициента корреляции r и его значимость.

# 4. Проверить адекватность модельного уравнения регрессии y на x, записанного через коэффициент корреляции r.

# 5. Проверить надежность уравнения регрессии y на x, записанного через коэффициент корреляции r и его коэффициентов.

# 6. Построить уравнения регрессий в первоначальной системе координат.
