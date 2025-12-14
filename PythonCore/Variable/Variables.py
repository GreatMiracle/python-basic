"""
Variables
"""

first_name = "Eric"
print(first_name)
first_name = "Melissa"
print(first_name)
print('---------------------------------------------------------')

# File: variables.py

# Không dùng biến → khó hiểu
print(10)  # Output: 10

# Dùng biến → rõ ràng hơn
cost = 10          # int (số nguyên)
print(cost)        # Output: 10

# Hover trong PyCharm sẽ hiện type hint: cost: int = 10
print('---------------------------------------------------------')

# Ứng dụng thực tế: Tính giá có thuế:
cost = 10                  # Giá gốc
tax_percent = 0.25         # Thuế 25% (float - số thập phân)
tax = cost * tax_percent    # Tính tiền thuế
price = cost + tax         # Tổng giá

print(price)               # Output: 12.5
print('---------------------------------------------------------')

username = "coding with Ruby"   # Dùng nháy kép hoặc nháy đơn đều được
first_name = "Eric"

print(username)                 # Output: coding with Ruby

# Nối chuỗi (concatenation)
full_name = username + " " + first_name
print(full_name)                # Output: coding with Ruby Eric

# Nếu không thêm khoảng trắng:
print(username + first_name)    # Output: coding with RubyEric (dính liền)
print('---------------------------------------------------------')

first_num = 10
second_num = 2
print(first_num, second_num)   # Output: 10 2

first_num = 1                  # Gán lại → giá trị cũ mất
print(first_num, second_num)   # Output: 1 2

# Với string cũng vậy
name = "Eric"
print(name)                    # Eric

name = "Melissa"
print(name)                    # Melissa

print('---------------------------------------------------------')

print('----------------comment-----------------------------------------')
print('---------------- bôi đen shift + " hoặc '/'----------------------------------------')