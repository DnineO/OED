import matplotlib.pyplot as plt
import math

# Даны значения ширины пера круглой плашки(в мм)
AArray = [3.69, 3.56, 3.52, 3.68, 3.49, 3.58, 3.59, 3.54, 3.35, 3.69, 3.87, 3.67, 3.79,
          3.75, 3.43, 3.50, 3.57, 3.53, 3.49, 3.68, 3.36, 3.63, 3.51, 3.99, 3.90, 3.53,
          3.50, 3.55, 3.40, 3.73, 3.72, 3.53, 3.42, 3.72, 3.68, 3.46, 3.46, 3.36, 3.37,
          3.53, 3.48, 3.70, 3.48, 3.68, 3.46, 3.61, 3.57, 3.47, 3.74, 3.47]

# Вычислим размах варьирования признака X
Xmax = max(AArray)
Xmin = min(AArray)
R = Xmax - Xmin
print("Xmax = ", Xmax)
print("Xmin = ", Xmin)
print("R = ", R)
n = len(AArray)
print("n = ",n)

# Определим число интервалов k
k = len(AArray) ** 0.5
print("k = ", k)

# Найдем длину(h) частичных интервалов
h = R/k
print("h = ", h)

# Подсчитаем число вариант, попадающих в каждый интервал
XArray = []
NArray = []
X0 = Xmin - 0.5 * h      # начало первого интервала
Xk = Xmax + 0.5 * h      # конец последнего интервала

i = 0
XArray.append(X0)
while XArray[i] < Xk:
    i += 1
    prom = XArray[i-1] + h
    XArray.append(prom)
    # print("%.2f" % XArray[i], " ", i)

for i in range(len(XArray)):
    count = 0
    for j in range(len(AArray)):
        if XArray[i] <= AArray[j] < XArray[i+1]:
            count += 1
    NArray.append(count)

# Контроль

# summ = 0
# for i in range(len(NArray)):
#     summ += (NArray[i])
# if summ == len(AArray):
#     print("Control = All good")
# else:
#     print("Control = All bad")

# Запишем дискретный вариационный ряд

XiArray = []
Xi_Array = []
for i in range(9):
    Xi = (XArray[i] + XArray[i+1]) / 2 
    XiArray.append(Xi)
XiArray.append(0)
for i in range(8):
    if i == 8:
        break
    print("%.2f - %.2f : n = %.f, Xi = %.2f" % (XArray[i], XArray[i + 1], NArray[i], XiArray[i]))

# Изобразим вариационные ряды графически
# plt.xlabel('Интервалы')
# plt.ylabel('h')
# plt.title('Вариационный ряд')
# plt.grid(True)
# plt.bar(XArray[:-1], NArray[:-1], h - 0.001)
# plt.plot(XArray[:-1], NArray[:-1], color="black")
# plt.show()

# Построим кумуляту
WArray = []
wArray = [0]

for i in range(len(XiArray)):
    wArray.append(NArray[i]/n)
    if i == 0:
        WArray.append(wArray[i])
    else:
        WArray.append(WArray[i-1]+wArray[i])


# Найдем эмпирическую функцию
EmpArray = []
Nx = 0
for i in range(len(XArray)):
    EmpArray.append(Nx / n)
    Nx += NArray[i] 

# plt.title('Кумулята и эмперическая функция распределения')
# plt.xlabel('Варианты')
# plt.ylabel('Частоты')
# plt.bar(XiArray[:-1],EmpArray[:-1], h-0.01)
# plt.plot(XiArray[:-1], WArray[:-1], color = "red")
# plt.show()

# Вычислить моду, медиану, выборочную среднюю, выборочную
# дисперсию, выборочное среднее квадратическое отклонение, коэффициент вариации, асимметрию, эксцесс.
Nmax = max(NArray)
UiArray = []
for i in range(len(XiArray)):
    if Nmax == NArray[i]:
        MoX = XiArray[i-1]
        MeX = (MoX + XiArray[i])/2
for i in range(len(XiArray)-1):
    UiArray.append((XiArray[i]-MoX)/h)

# Найдем условные начальные моменты
M1 = 0
M2 = 0
M3 = 0
M4 = 0

for i in range(len(UiArray)):
    M1 += (NArray[i] * UiArray[i])
    M2 += (NArray[i] * UiArray[i]) ** 2
    M3 += (NArray[i] * UiArray[i]) ** 3
    M4 += (NArray[i] * UiArray[i]) ** 4
# print(M1,M2,M3,M4)
M1 /= n
M2 /= n
M3 /= n
M4 /= n
# print(M1,M2,M3,M4)

# Найдем выборочную среднюю
AverX = M1 * h + MoX
# Найдем выборочную дисперсию
Dispertion = (M2 - M1**2) * h**2
# Вычислим выборочное средне квадратичное отклонение
AverDeviation = math.sqrt(Dispertion)
# Вычислим коэффициент вариации
VariationCoef = AverDeviation / AverX
# Найдем центральные моменты третьего и четвертого порядков
m3 = (M3 - 3 * M2 * M1 + 2 * M1 ** 3) * h ** 3
m4 = (M4 - 4 * M3 * M1 + 6 * M2 * M1 ** 2 - 3 * M1 ** 4) * h ** 4
# Найдем ассиметрию и эксцесс
As = m3 / AverDeviation ** 3
Ex = m4 / AverDeviation ** 4 - 3

# Построим доверительные интервалы для истинного значения измеряемой величины и
# среднего квадратического отклонения генеральной совокупности.
t = 2.009  # y = 0.95 по таблице Лапласа
buf = AverDeviation / math.sqrt(n) * t
# Доверительный интервал:
min1 = AverX - buf
max1 = AverX + buf
q = 0.21  # y = 0.95 по таблице Лапласа
min2 = AverDeviation * (1 - q)
max2 = AverDeviation * (1 + q)

# print(f"{round(min1, 2)} < a < {round(max1, 2)}")
# print(f"{round(min2, 2)} < S < {round(max2, 2)}")

# на основе дискретного вариационного ряда, полученного в лабораторной работе № 1, выполнить следующее:
# Построить эмпирическую (полигон) и теоретическую (нормальную) кривую распределения.
# Проверить согласованность эмпирического распределения с теоретическим нормальным, применяя три критерия:
# а) критерий Пирсона;
# б) один из критериев: Колмогорова, Романовского, Ястремского;
# в) приближенный критерий.

# рассчитаем теоретические частоты
NDotArray = []
# PhiArray = [0.3251, 0.3778, 0.3932, 0.3989, 0.3945, 0.3802, 0.3555, 0.3251, 0.2874, 0.2492]

for i in range(len(XArray)):
    ui = (XArray[i] - AverX) / AverDeviation
    phi = round((1 / math.sqrt(2 * math.pi)) * math.exp(-1 * ui ** 2 / 2), 4)
    yi = ((n * h) / AverDeviation) * phi
    NDotArray.append(round(yi, 0))
    print(f"ui = {round(ui, 2)}, n'i = {NDotArray[i]}, {round(yi, 4)}, phi = {phi}")
print("S = ", AverDeviation)

x_2 = 0
for i in range(len(NDotArray)):
    x_2 += (NArray[i] - NDotArray[i]) ** 2 / NDotArray[i]
# print("X^2 = ", x_2)

# а) критерий Пирсона
# число степеней свободы (k)
number_degrees_freedom = 7
# находим по приложению 5
x_kr = 2.17
if x_kr < x_2:
    print("Гипотеза о нормальном распределении признака Х отвергается")
else:
    print("Нет достаточных оснований отвергнуть выдвинутую гипотезу")
# б) критерий Романовского
crit = abs((x_2 - number_degrees_freedom)/ math.sqrt(2 * number_degrees_freedom))
if crit < 3:
    print("Данное эмпирическое распределение подчиняется нормальному распределению")
else:
    print("Нет оснований считать что эмпирическое распределение подчиняется нормальному закону распределения")

# в) приближенный критерий
Sas = math.sqrt((6*(n - 1))/((n + 1)*(n + 3)))
Sex = math.sqrt((24 * n * (n - 2)*(n - 3))/((n-1)**2 * (n + 3) * (n + 5)))
if Sas < As and Sex < Ex:
    print("Выборочная совокупность не будет распределена по нормальному закону")
print(round(Sas,3),"<",round(As,3),"|",round(Sex,3),"<",round(Ex,3))

plt.title('Вариационный ряд')
plt.xlabel('Варианты')
plt.ylabel('Частоты')
plt.plot(XArray[:-1], NArray[:-1], color="black")
plt.plot(XArray[:-1], NDotArray[:-1], linestyle=':')
plt.show()
