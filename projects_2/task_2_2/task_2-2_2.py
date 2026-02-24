user_input=input("Введи ченить")
raw_data = "  atgcatgc  "
processed_input = raw_data.strip().upper()
print(f"Вот: {user_input},\t{processed_input}", sep= "->")