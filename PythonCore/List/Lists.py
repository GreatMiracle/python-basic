my_list = [80, 96, 72, 100, 8]      # List số (int)
print(my_list)                      # Output: [80, 96, 72, 100, 8]


people_list = ["Eric", "Adele", "Jeff"]  # List chuỗi (str)
print(people_list)                  # Output: ['Eric', 'Adele', 'Jeff']

# List hỗn hợp (mixed)
mixed_list = [1, "hello", 3.14, True]
print(mixed_list)

print(my_list[0])    # 80 (phần tử đầu)
print(my_list[1])    # 96
print(my_list[-1])   # 8 (phần tử cuối – siêu tiện!)
print(my_list[-2])   # 100

# Lỗi nếu index vượt quá: my_list[5] → IndexError: list index out of range

# Thay đổi phần tử:
people_list[0] = "Mel"              # Thay Eric thành Mel
print(people_list)                  # ['Mel', 'Adele', 'Jeff']

# Độ dài list:
print(len(people_list))             # 3 (số phần tử thực tế, không phải index max)

# Slicing (cắt lát) – Lấy một phần list:
print('Slicing (cắt lát) – Lấy một phần list: list[start : end] - KHÔNG bao gồm end')
print(my_list[0:2])     # [80, 96] → từ index 0 đến trước 2 (không bao gồm 2)
print(my_list[2:])      # [72, 100, 8] → từ index 2 đến hết
print(my_list[:4])      # [80, 96, 72, 100] → từ đầu đến trước 4
print(my_list[-3:])     # [72, 100, 8] → 3 phần tử cuối
print(my_list[::-1])    # [8, 100, 72, 96, 80] → đảo ngược list (step -1)

print('Các method phổ biến:')
my_list.append(1000)          # Thêm cuối
print(my_list)                # [80, 96, 72, 100, 8, 1000]

my_list.insert(2, 999)        # Chèn vào index 2
print(my_list)                # [80, 96, 999, 72, 100, 8, 1000]

my_list.remove(8)             # Xóa giá trị 8 (phần tử đầu tiên tìm thấy)
my_list.pop(0)                # Xóa và trả về phần tử index 0 (80)

my_list.sort()                # Sắp xếp tăng dần (chỉ cùng kiểu)
print(my_list)                # [72, 96, 99, 100, 1000]

my_list.sort(reverse=True)    # Giảm dần