def kiem_tra_chan_le(n):
    return "Chẵn" if n % 2 == 0 else "Lẻ"

def kiem_tra_nam_nhuan(y):
    return "Năm nhuận" if (y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)) else "Không phải năm nhuận"

def kiem_tra_so_100(n):
    return "Lớn hơn 100" if n > 100 else "Nhỏ hơn hoặc bằng 100"

def tinh_thue(thu_nhap):
    if thu_nhap <= 5000000:
        return "Thuế 5%"
    elif thu_nhap <= 10000000:
        return "Thuế 10%"
    else:
        return "Thuế 20%"

def xep_loai_hoc_luc(dtb):
    if dtb >= 8:
        return "Giỏi"
    elif dtb >= 6.5:
        return "Khá"
    elif dtb >= 5:
        return "Trung bình"
    else:
        return "Yếu"

def chia_het_3_va_5(n):
    return "Chia hết cho cả 3 và 5" if n % 3 == 0 and n % 5 == 0 else "Không chia hết"

def xac_dinh_giai_doan_tuoi(tuoi):
    if tuoi < 12:
        return "Trẻ em"
    elif tuoi < 18:
        return "Thanh niên"
    elif tuoi < 60:
        return "Người lớn"
    else:
        return "Người già"

def la_tam_giac(a, b, c):
    return "Là tam giác" if a + b > c and a + c > b and b + c > a else "Không phải tam giác"

def nguyen_am_hay_phu_am(ch):
    return "Nguyên âm" if ch.lower() in 'aeiou' else "Phụ âm"

def kiem_tra_ngay_hop_le(ngay, thang, nam):
    from datetime import datetime
    try:
        datetime(nam, thang, ngay)
        return "Hợp lệ"
    except ValueError:
        return "Không hợp lệ"

def tinh_tong_1_den_100():
    return sum(range(1, 101))

def in_bang_cuu_chuong(n):
    return [f"{n} x {i} = {n * i}" for i in range(1, 11)]

def tinh_giai_thua(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def so_nguyen_to_nho_hon(N):
    primes = []
    for num in range(2, N):
        if all(num % i != 0 for i in range(2, int(num**0.5) + 1)):
            primes.append(num)
    return primes

def in_tam_giac_sao(h):
    return "\n".join("*" * (i + 1) for i in range(h))

def so_armstrong(n):
    digits = [int(d) for d in str(n)]
    return "Là số Armstrong" if sum(d**len(digits) for d in digits) == n else "Không phải số Armstrong"

def dao_nguoc_so(n):
    return int(str(n)[::-1])

def tong_cac_chu_so(n):
    return sum(int(d) for d in str(n))

def dem_tu_xuat_hien(s, word):
    return s.lower().split().count(word.lower())

# Nhập dữ liệu từ người dùng và chạy các hàm
n = int(input("Nhập một số để kiểm tra chẵn/lẻ: "))
print(kiem_tra_chan_le(n))

y = int(input("Nhập một năm để kiểm tra năm nhuận: "))
print(kiem_tra_nam_nhuan(y))

print("Tổng các số từ 1 đến 100:", tinh_tong_1_den_100())

n = int(input("Nhập một số để in bảng cửu chương: "))
print("\n".join(in_bang_cuu_chuong(n)))

n = int(input("Nhập một số để tính giai thừa: "))
print(tinh_giai_thua(n))

n = int(input("Nhập một số để tìm Fibonacci thứ n: "))
print(fibonacci(n))

N = int(input("Nhập một số để tìm các số nguyên tố nhỏ hơn N: "))
print(so_nguyen_to_nho_hon(N))

h = int(input("Nhập chiều cao tam giác sao: "))
print(in_tam_giac_sao(h))

n = int(input("Nhập một số để kiểm tra số Armstrong: "))
print(so_armstrong(n))

n = int(input("Nhập một số để đảo ngược: "))
print(dao_nguoc_so(n))

n = int(input("Nhập một số để tính tổng chữ số: "))
print(tong_cac_chu_so(n))

s = input("Nhập một câu: ")
word = input("Nhập từ cần đếm: ")
print(dem_tu_xuat_hien(s, word))
