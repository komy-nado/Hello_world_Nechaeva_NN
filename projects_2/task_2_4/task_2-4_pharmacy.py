total_capsules=int(input("Введите общее количество произведенных капсул: "))
capsuls_amount=int(input("Введите количество капсул в одной упаковке: "))
full_packs=total_capsules // capsuls_amount
remainder=total_capsules % capsuls_amount
print("\n Отчет фасовочного цеха ")
print(f"Полных упаковок:\t{full_packs}")
print(f"Остаток капсул:\t\t{remainder}")