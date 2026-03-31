import numpy as np

n = int(input("Nhập số phần tử n: "))
a = np.random.randint(1, 100, n) 
filter_arr = (a % 2 == 0) 
b = a[filter_arr]
print("Mảng a:", a)
print("Mảng b (các phần tử chẵn):", b)