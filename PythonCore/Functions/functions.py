# File: functions.py

print('----------Định nghĩa và gọi hàm cơ bản:----------------')
def my_function():                  # def = define hàm
    print("Inside my function!")

# Gọi hàm
my_function()                       # Output: Inside my function!

print('----------Hàm có tham số (parameters)::----------------')
def print_name(name):               # name là parameter
    print(f"Hello {name}")

print_name("Eric")                  # Output: Hello Eric
print_name("Steve Jobs")            # Có thể gọi nhiều lần với giá trị khác

def print_full_name(first_name, last_name):
    print(f"Hello {first_name} {last_name}")

print_full_name("Steve", "Jobs")    # Output: Hello Steve Jobs

print('Gọi với tên tham số rõ ràng (keyword arguments – rất khuyến khích):')
print_full_name(last_name="Jobs1", first_name="Steve1")  # Thứ tự không quan trọng

print('--------------Hàm trả về giá trị bằng return:-------------')
def multiply_numbers(a, b):
    return a * b                    # Trả về kết quả, không chỉ print

solution = multiply_numbers(10, 6)
print(solution)                     # 60

print('--------------Scope (Phạm vi biến) – Global vs Local:---------------')
color = "blue"                      # Global variable

def print_color_red():
    color = "red"                   # Local variable – chỉ tồn tại trong hàm
    print(color)                    # red

print(color)                        # blue (global)
print_color_red()                   # red (local)
print(color)                        # vẫn là blue (local không ảnh hưởng global)

print('-------------------Hàm gọi hàm khác (rất phổ biến):----------------')
def add_tax(cost):
    tax_rate = 0.03
    return cost * tax_rate

def buy_item(cost):
    return cost + add_tax(cost)     # Gọi hàm con

final_cost = buy_item(50)
print(final_cost)                   # 51.5

print('---------------Hàm xử lý list:-------------------')
def print_list(numbers):
    for x in numbers:
        print(x)

numbers_list = [1, 2, 3, 4, 5]
print_list(numbers_list)            # In từng số