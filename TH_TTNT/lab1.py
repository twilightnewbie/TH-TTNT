a = float(input("Nhap gia tri a"))
b= float(input("Nhap gia tri b"))
tong = a + b
hieu = a - b
thuong = a / b
tich = a * b
print("Tong a va b la: ", tong)
print("Hieu a va b la:", hieu)
print("Thuong a va b la:", thuong)
print("tich a va b la:", tich)
if b != 0:
    thuong = a / b
    print(f"Thương của {a} và {b} là: {thuong}")
else:
    print("Không thể tính thương vì số chia (b) bằng 0.")