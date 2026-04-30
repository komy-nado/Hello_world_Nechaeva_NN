n = int(input("Введите циферку: "))

def sum_n(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

print("Да вот сумма, вот, только отстать, людь 👹", sum_n(n))