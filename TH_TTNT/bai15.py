import datetime

class SinhVien:
    def __init__(self, ma_sv, ten, nam_sinh, dtb):
        self.ma_sv = ma_sv[:10] 
        self.ten = ten[:20]     
        self.nam_sinh = int(nam_sinh) 
        self.dtb = float(dtb)    

    def __str__(self):
        return f"MSV: {self.ma_sv} | Tên: {self.ten} | Năm sinh: {self.nam_sinh} | ĐTB: {self.dtb}"
    def nhap_danh_sach_sv(n):
        ds_sv = []
        for i in range(n):
            print(f"Nhập thông tin sinh viên thứ {i+1}:")
            ma = input("Mã SV: ")
            ten = input("Tên SV: ")
            nam = int(input("Năm sinh: "))
            diem = float(input("Điểm TB: "))
            ds_sv.append(SinhVien(ma, ten, nam, diem))
        return ds_sv
    def dem_sv_len_lop(ds_sv):
        count = sum(1 for sv in ds_sv if sv.dtb >= 5)
        return count
    def xuat_sv_20_tuoi(ds_sv):
        nam_hien_tai = datetime.datetime.now().year
        print("Danh sách sinh viên đủ 20 tuổi:")
        for sv in ds_sv:
            if nam_hien_tai - sv.nam_sinh >= 20:
                print(sv)
    def dem_sv_he_dh(ds_sv):
        count = 0
        for sv in ds_sv:
            if sv.ma_sv[2:4].upper() == "DH":
                count += 1
        return count
    def dem_ten_lan(ds_sv):
        return sum(1 for sv in ds_sv if sv.ten.split()[-1].lower() == "lan")

    def dem_ho_phan(ds_sv):
        return sum(1 for sv in ds_sv if sv.ten.split()[0].lower() == "phan")
    n = int(input("Nhập số lượng sinh viên: "))
    danh_sach = nhap_danh_sach_sv(n)

    print(f"\nSố SV đủ điều kiện lên lớp: {dem_sv_len_lop(danh_sach)}")
    xuat_sv_20_tuoi(danh_sach)
    print(f"Số SV hệ Đại học: {dem_sv_he_dh(danh_sach)}")
    print(f"Số SV tên Lan: {dem_ten_lan(danh_sach)}")
    print(f"Số SV họ Phan: {dem_ho_phan(danh_sach)}")