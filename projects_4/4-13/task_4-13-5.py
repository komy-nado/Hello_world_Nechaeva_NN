n = int(input("Сколько цмферк вам подсказывает Ктулх: "))

mx_num = None

for i in range(n):
    num = int(input(f"Введите циферк {i + 1}: "))
    
    if mx_num is None or num > mx_num:
        max_num = num

print("Самый большой циферк", mx_num)