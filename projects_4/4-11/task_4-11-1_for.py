a = [1, 2, 3]
b = [4, 5, 6]
n = len(a)

scal = 0

for i in range(n):
    scal = scal + a[i] * b[i]

print("Скалярное произведение двух векторов:", scal)