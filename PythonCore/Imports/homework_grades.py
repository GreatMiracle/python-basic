# Import hàm từ file khác
import grade_average_service as grade_service   # Dùng "as" để đặt tên ngắn

homework_assignment_grades = {
    "homework_1": 85,
    "homework_2": 100,
    "homework_3": 81
}

result = grade_service.calculate_homework(homework_assignment_grades)
print(result)   # Output: 88.67

print('-----------------Import từ Python Standard Library----------------')
# random.py
import random

drinks = ["soda", "coffee", "water", "tea"]
print(random.choice(drinks))        # Mỗi lần chạy ra một đồ uống ngẫu nhiên

print(random.randint(1, 10))        # Số nguyên ngẫu nhiên từ 1 đến 10


# math_example.py
import math

print(math.sqrt(64))                # 8.0
print(math.pi)                      # 3.141592653589793
print(math.factorial(5))            # 120
print(math.degrees(math.pi))        # 180.0

from math import sqrt, pi           # Chỉ import những gì cần
print(sqrt(25))                     # 5.0

from random import choice as pick   # Đặt alias cho hàm
print(pick(["apple", "banana"]))