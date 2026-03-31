import numpy as np

def tao_mang(m, n):
    return np.random.randint(1, 101, size=(m, n))

def xuat_dong_k(a, k):
    if k < a.shape[0]:
        print(f"Các phần tử thuộc dòng {k}: {a[k, :]}") # Cú pháp slicing dòng 
    else:
        print("Chỉ số dòng không hợp lệ")

def xuat_cot_k(a, k):
    if k < a.shape[1]:
        print(f"Các phần tử thuộc cột {k}: {a[:, k]}") # Cú pháp slicing cột 
    else:
        print("Chỉ số cột không hợp lệ")

def dong_tong_lon_nhat_45(a):
    tong_cac_dong = a.sum(axis=1) # Tính tổng theo từng dòng
    dong_thoa_man = tong_cac_dong[tong_cac_dong <= 45]
    if dong_thoa_man.size > 0:
        max_val = dong_thoa_man.max()
        index = np.where(tong_cac_dong == max_val)[0]
        print(f"Dòng có tổng lớn nhất (<=45) là dòng {index} với tổng = {max_val}")
    else:
        print("Không có dòng nào có tổng <= 45")

def cot_tich_nho_nhat(a):
    tich_cac_cot = a.prod(axis=0) 
    index_min = np.argmin(tich_cac_cot)
    print(f"Cột có tích nhỏ nhất là cột {index_min} với tích = {tich_cac_cot[index_min]}")

def dong_chan_cot_le(a):
    kq = a[0::2, 1::2]
    print("Các phần tử thuộc dòng chẵn và cột lẻ:\n", kq)

def tbc_chan_dong_le(a):
    dong_le = a[1::2, :] 
    phan_tu_chan = dong_le[dong_le % 2 == 0] 
    if phan_tu_chan.size > 0:
        print(f"Trung bình cộng phần tử chẵn thuộc dòng lẻ: {phan_tu_chan.mean()}")
    else:
        print("Không có phần tử chẵn nào ở dòng lẻ")

def tbc_bien(a):
    m, n = a.shape
    mask = np.ones((m, n), dtype=bool)
    mask[1:-1, 1:-1] = False 
    bien = a[mask]
    print(f"Trung bình cộng các phần tử biên: {bien.mean()}")

def trung_binh_tich_loi(a):
    loi = a[1:-1, 1:-1]  
    if loi.size > 0:
        tich = loi.prod()
        print(f"Tích các phần tử lõi: {tich}")
    else:
        print("Ma trận quá nhỏ, không có phần tử lõi")

m, n = 4, 5
mang_a = tao_mang(m, n)
print("Ma trận a:\n", mang_a)

xuat_dong_k(mang_a, 1)
dong_tong_lon_nhat_45(mang_a)
cot_tich_nho_nhat(mang_a)
dong_chan_cot_le(mang_a)
tbc_chan_dong_le(mang_a)
tbc_bien(mang_a)
trung_binh_tich_loi(mang_a)