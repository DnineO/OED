import matplotlib.pyplot as plt

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
    print("%.2f" % XArray[i], " ", i)

for i in range(len(XArray)):
    count = 0
    for j in range(len(AArray)):
        if XArray[i] <= AArray[j] < XArray[i+1]:
            count += 1
    NArray.append(count)

# Контроль
summ = 0
for i in range(len(NArray)):
    summ += (NArray[i])
if summ == len(AArray):
    print("Control = All good")
else:
    print("Control = All bad")

# Запишем дискретный вариационный ряд
XiArray = []
for i in range(8):
    Xi = (XArray[i] + XArray[i+1]) / 2
    XiArray.append(Xi)
XiArray.append(0)
XiArray.append(0)
for i in range(8):
    if i == 8:
        break
    print("%.2f - %.2f : n = %.f, Xi = %.2f" % (XArray[i], XArray[i + 1], NArray[i], XiArray[i]))

# Изобразим вариационные ряды графически
plt.xlabel('Интервалы')
plt.ylabel('h')
plt.title('Заголовок')
plt.grid(True)
plt.bar(XArray, NArray, h - 0.001)
plt.plot(XArray, NArray, color="black")
plt.show()

# Построим кумуляту
WArray = []
wArray = []

for i in range(len(XiArray)):
    wArray.append(NArray[i]/n)
    if i == 0:
        WArray.append(wArray[i])
    else:
        WArray.append(WArray[i-1]+wArray[i])

plt.title('Кумулятивная кривая')
plt.xlabel('Варианты')
plt.ylabel('Накопительные частоты')
plt.grid()
plt.plot(XArray, WArray, color="red")
plt.show()