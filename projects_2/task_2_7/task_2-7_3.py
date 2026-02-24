sequences=["ATATACGCGTA", "CTTCGGNGGA"]
for seq in sequences:
    print(f"Полная последовательность: {seq}")   
    print("Построчный вывод:")
    for nucleotide in seq:
        print(nucleotide)
    print("-" * 10)
print("Цикл выполнен")