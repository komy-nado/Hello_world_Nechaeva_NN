opr_name=input("Введите имя оператора: ")
prssr_snsr_data=input("Укажите текущее значение датчика давления: ")
with open("sensor_log.txt", "w", encoding="utf-8") as report:
    report.write(f"Имя оператора:\t {opr_name}\n")
    report.write(f"Значение датчика давления:\t {prssr_snsr_data}\n")
print("Данные успешно сохранены в sensor_log.txt")