# Dictionary = key → value

print('-----------------Tạo dict và in ra:---------')
# File: dictionaries.py

user_dict = {
    "username": "coding with Ruby",
    "name": "Eric",
    "age": 32
}

print(user_dict)
# Output: {'username': 'coding with Ruby', 'name': 'Eric', 'age': 32}

print('-------Truy cập giá trị bằng key:------------')
print(user_dict["username"])      # coding with Ruby
print(user_dict.get("age"))       # 32 (get() an toàn hơn nếu key không tồn tại)
# print(user_dict["email"])       # Lỗi KeyError nếu key không có
print(user_dict.get("email", "Không có"))  # Không có (giá trị mặc định)


print('--------------Thêm/sửa phần tử:----------------')
user_dict["married"] = True       # Thêm key mới
user_dict["age"] = 33             # Sửa value cũ
print(user_dict)
# {'username': ..., 'name': ..., 'age': 33, 'married': True}


print('---------Các method phổ biến:-------------')
print(len(user_dict))             # 4 (số cặp key-value)

user_dict.pop("age")              # Xóa key "age" và trả về value
print(user_dict)                  # age đã mất

# user_dict.clear()                 # Xóa hết → {}
# del user_dict                   # Xóa luôn biến dict (sau đó print sẽ lỗi)

print('-------------------Lặp qua dict:-----------------')
# Chỉ keys (mặc định)
for key in user_dict:
    print(key)                    # username, name, age...

# Keys rõ ràng
for key in user_dict.keys():
    print(key)

# Values
for value in user_dict.values():
    print(value)

print('>>>>>Cả key và value (phổ biến nhất)')
for key, value in user_dict.items():
    print(f"{key}: {value}")