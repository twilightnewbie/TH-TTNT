def tron_mang(a, b):
    min_len = len(a) if len(a) < len(b) else len(b)
    
    res = b[:] if len(b) > len(a) else a[:]
    
    for i in range(min_len):
        res[i] = a[i] + b[i]
        
    return res
a = [3, 9, 1, 4]
b = [2, 7, 4, 3, 2, 8]
print("Mảng a:", a)
print("Mảng b:", b)
print("Mảng kết quả:", tron_mang(a, b))