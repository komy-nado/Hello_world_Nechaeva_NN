n = int(input("Введите циферфырфки "))
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print("ДА ВОТ ТЕБЕ ФКТОРИАЛ, ОТСТАНЬ ЧЕЛОВЕК! 🤬", factorial(n))