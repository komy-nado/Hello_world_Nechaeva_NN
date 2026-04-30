arr = [7, 3, 8, 1, 4, 6, 2, 5]
n = len(arr)

for i in range(n):
    swapped = False  # Флаг: была ли перестановка?
    for j in range(0, n - i - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            swapped = True     
    
    if not swapped:
        break

print("Во какой массив красивый:", arr)