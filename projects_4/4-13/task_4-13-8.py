arr = list(map(int, input("Введите циферки через пробел: ").split()))

count_positive = 0
for num in arr:
    if num > 0:
        count_positive += 1

print("Кол-во положительных циферкафф: ", count_positive)