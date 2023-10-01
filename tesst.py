so_bat_ky = 0.000012354

# Chuyển số thành chuỗi
so_chuoi = str(so_bat_ky)

# Loại bỏ các số 0 ở đầu chuỗi
so_chuoi_khong_leading_zeros = so_chuoi.lstrip('0')

# Lấy 3 chữ số đầu tiên
if '.' in so_chuoi_khong_leading_zeros:
    so_chuoi_khong_leading_zeros, phan_thap_phan = so_chuoi_khong_leading_zeros.split('.')
    so_3_chu_so = so_chuoi_khong_leading_zeros[:3]
    ket_qua = f"{so_3_chu_so}.{phan_thap_phan}"
else:
    ket_qua = so_chuoi_khong_leading_zeros

print(ket_qua)
