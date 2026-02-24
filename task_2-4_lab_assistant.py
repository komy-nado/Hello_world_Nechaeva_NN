volume=float(input("Введите необходимый объем раствора (мл): "))
salt_mass=volume * 0.009
water_volume=volume
recipe_text=(
    "ОТЧЕТ ПО ПРИГОТОВЛЕНИЮ:\n"
    "-----------------------\n"
    f"Общий объем: {volume} мл\n"
    f"Масса соли:  {salt_mass:.2f} г\n"
    f"Объем воды:  {water_volume} мл"
)

with open("recipe.txt", "w", encoding="utf-8") as file:
    file.write(recipe_text)
print("\nРецепт успешно сохранен в файл recipe.txt")

