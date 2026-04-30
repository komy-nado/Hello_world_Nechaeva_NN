arr = list(map(int, input("Введите циферки через пробел: ").split()))

sum_odd_ind = 0
for i in range(len(arr)):
    if i % 2 != 0:
        sum_odd_ind += arr[i]

print("Сумма элементов с нечётными индексами:", sum_odd_ind)