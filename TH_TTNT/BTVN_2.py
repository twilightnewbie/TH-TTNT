import numpy as np

def tong_tam_giac_tren_phu(a):
    n = a.shape[0]
    tong = 0
    for i in range(n):
        for j in range(n):
            if i + j <= n - 1:
                tong += a[i, j]
    return tong

def tri_tuyet_doi(a):
    return np.abs(a)

def thay_chan_bang_x(a, x):
    a[a % 2 == 0] = x
    return a
def kiem_tra_toan_chan(a):
    return np.all(a % 2 == 0)
def kiem_tra_doi_xung(a):
    return np.array_equal(a, a.T)

def duong_cheo_chinh_tang_dan(a):
    d_cheo = np.diag(a) 
    return np.all(np.diff(d_cheo) > 0)

def xuat_tam_giac_duoi_phu(a):
    n = a.shape[0]
    print("Các phần tử tam giác dưới đường chéo phụ:")
    for i in range(n):
        for j in range(n):
            if i + j >= n - 1:
                print(a[i, j], end=" ")
        print()

def duong_cheo_phu_giam_dan(a):
    n = a.shape[0]
    d_cheo_phu = np.diag(np.fliplr(a))
    return np.all(np.diff(d_cheo_phu) < 0)