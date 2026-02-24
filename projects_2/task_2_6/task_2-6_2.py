ph_value=float(input("Введите значение pH (от 0 до 14): "))
if ph_value < 7:
    print("Результат: Среда кислотная")
elif ph_value == 7:
    print("Результат: Среда нейтральная")
elif ph_value <= 14:
    print("Результат: Среда щелочная")
else:
    print("!Ошибка: Значение pH не должно превышать 14!")