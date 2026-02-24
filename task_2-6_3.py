Don_group=input("Введите группу крови донора (в системе A, B, 0): ").strip().upper()
pat_group=input("Введите группу крови пациента (в системе A, B, 0): ").strip().upper()
if Don_group == pat_group or Don_group == "0":
    print("\n Результат: Переливание разрешено.")
    if Don_group == "0" and pat_group != "0":
        print("Примечание: Используется универсальная донорская группа (0).")
else:
    print("\n Результат: Переливание запрещено!")
    print(f"Группа {Don_group} не подходит для пациента с группой {pat_group}.")