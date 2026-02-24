product_name=input("Введите название питательной среды: ")
concentration=input("Укажите концентрацию агара (%): ")
tempr=input("Поведайте температуру стерилизации: ")
with open("recipe.txt", "w", encoding="utf-8") as report:
    report.write(f"Название среды:\t{product_name}\n")
    report.write(f"Концентрация:\t{concentration}\n")
    report.write(f"Температура:\t{tempr}\n")