
print('Sets – Tập hợp (unordered, unique):::::::::::::::::')
my_set = {1, 2, 3, 4, 5, 1, 2}      # Trùng lặp sẽ bị loại
print(my_set)                       # Output: {1, 2, 3, 4, 5} (không thứ tự cố định)

print(len(my_set))                  # 5 (chỉ đếm unique)

# Không truy cập bằng index
# print(my_set[0])                  # Lỗi: TypeError: 'set' object is not subscriptable

# Thêm phần tử
my_set.add(6)
print(my_set)                       # {1, 2, 3, 4, 5, 6}

# Thêm nhiều phần tử
my_set.update([7, 8])
print(my_set)

# Xóa phần tử
my_set.discard(3)                   # Xóa 3 (nếu không có thì không lỗi)
my_set.remove(4)                    # Xóa 4 (nếu không có thì lỗi)

my_set1 = {1, 2, 3, 4, 5, 1, 2}
my_set1.clear()                      # clear() – xoá toàn bộ
print(my_set1)



print('Tuples – Bộ giá trị (ordered, immutable):::::::::::')

my_tuple = (1, 2, 3, 4, 5)
print(my_tuple)                     # (1, 2, 3, 4, 5)
print(len(my_tuple))                # 5

print(my_tuple[1])                  # 2 (có index)
print(my_tuple[-1])                 # 5 (phần tử cuối)

# Không thể thay đổi
# my_tuple[0] = 100                 # Lỗi: TypeError: 'tuple' object does not support item assignment
# my_tuple.append(6)                # Lỗi: AttributeError

# Có thể tạo tuple 1 phần tử (phải có dấu phẩy)
single = (5,)                       # tuple
not_tuple = (5)                     # chỉ là int