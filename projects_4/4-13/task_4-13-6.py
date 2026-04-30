n = int(input("Введите циферку: "))

total = 0
for i in range(1, n + 1):
    total += i ** 2

print("Сумма квадратов:", total)