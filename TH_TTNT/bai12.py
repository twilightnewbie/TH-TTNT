
tong = 0

for i in range(1000):
    if i % 3 == 0 or i % 5 == 0:
        tong += i

print(f"Tổng các số từ 0 đến 999 là bội của 3 hoặc 5 là: {tong}")