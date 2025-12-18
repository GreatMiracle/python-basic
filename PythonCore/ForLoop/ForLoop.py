# File: loops.py

print('--------------------Vòng lặp for – Lặp qua iterable-------------------------')
my_list = [1, 2, 3, 4, 5]

# Cách thủ công (không nên)
print(my_list[0])
print(my_list[1])
# ... (dài dòng)

# Cách tốt: for loop
for num in my_list:
    print(num)          # Output: 1 2 3 4 5

# Iterator có thể đặt tên gì cũng được (thường dùng x, item, value)
for x in my_list:
    print(x)


print('-------------------Lặp qua string:--------------')
for char in "Python":
    print(char)         # P y t h o n

print('------------Lặp qua range (tạo dãy số):----------------------')
for i in range(3, 6):   # 3 đến 5 (không bao gồm 6)
    print(i)            # 3 4 5

for i in range(10):     # 0 đến 9
    print(i)

print('--------------Vòng lặp while – Lặp theo điều kiện--------------')
i = 0
while i < 5:
    i += 1
    print(i)            # 1 2 3 4 5

# Nếu quên i += 1 → loop vô hạn (crash máy!)

print('-----------break: Thoát hẳn vòng lặp.---------')
i = 0
while i < 10:
    if i == 4:
        break
    print(i)
    i += 1
# Output: 0 1 2 3 (dừng tại 4)

print('continue: Bỏ qua phần còn lại của lần lặp hiện tại, tiếp tục lần sau.')
i = 0
while i < 6:
    i += 1
    if i == 3:
        continue
    print(i)
# Output: 1 2 4 5 6 (bỏ qua 3)

print('else trong vòng lặp: Chạy khi vòng lặp kết thúc bình thường (không bị break).')
i = 0
while i < 5:
    i += 1
    print(i)
else:
    print("Vòng lặp kết thúc bình thường")  # Chạy khi i >= 5

print('-------------------------------')