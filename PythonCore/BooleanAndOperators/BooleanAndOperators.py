print('------------------Giá trị Boolean:----------------------')

is_active = True
is_deleted = False

print(is_active)    # True
print(type(True))   # <class 'bool'>

age = 25
score = 90

print(age == 25)    # True (bằng)
print(age != 30)    # True (khác)
print(score > 80)   # True (lớn hơn)
print(score < 100)  # True (nhỏ hơn)
print(age >= 18)    # True
print(score <= 89)  # False

print('------------------Toán tử logic (Logical operators) – Kết hợp nhiều biểu thức Boolean:')
# and: Cả hai phải True mới True
print(True and False)   # False
print(age > 18 and score >= 80)  # True (nếu cả hai đúng)

# or: Chỉ cần một True là True
print(True or False)    # True
print(age < 10 or score > 50)    # True

# not: Đảo ngược
print(not True)         # False
print(not (age == 25))  # False

print('------------Toán tử so sánh (Comparison operators) – Trả về True/False:-----------')
age = 25
score = 90

print(age == 25)    # True (bằng)
print(age != 30)    # True (khác)
print(score > 80)   # True (lớn hơn)
print(score < 100)  # True (nhỏ hơn)
print(age >= 18)    # True
print(score <= 89)  # False

print('-----------------Toán tử logic (Logical operators) – Kết hợp nhiều biểu thức Boolean:')
# and: Cả hai phải True mới True
print(True and False)   # False
print(age > 18 and score >= 80)  # True (nếu cả hai đúng)

# or: Chỉ cần một True là True
print(True or False)    # True
print(age < 10 or score > 50)    # True

# not: Đảo ngược
print(not True)         # False
print(not (age == 25))  # False