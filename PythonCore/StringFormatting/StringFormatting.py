# File: string_formatting.py

first_name = "Eric"

# Ghép bằng +
greeting = "Hi" + first_name          # Output: HiEric → thiếu space
greeting = "Hi1 " + first_name         # Output: Hi Eric → phải tự thêm space

print(greeting)                       # Hi Eric

print('------------------.format() method---------------------------------------')


first_name = "Eric"
last_name = "Robbie"

sentence = "Hi {} {}"                  # {} là placeholder
print(sentence.format(first_name, last_name))
# Output: Hi Eric Robbie

# Có thể đặt thứ tự rõ ràng
sentence2 = "Hi {0} {1}, welcome {0} again!"
print(sentence2.format(first_name, last_name))
# Output: Hi Eric Robbie, welcome Eric again!

# Hoặc dùng tên biến (named placeholders)
sentence3 = "Hi {fname} {lname}, I hope you are learning."
print(sentence3.format(fname=first_name, lname=last_name))
# Output: Hi Eric Robbie, I hope you are learning.

print('------------------------f-strings---------------------------------')
first_name = "Eric"
last_name = "Robbie"

# f-string cơ bản
print(f"Hi {first_name} {last_name}, I hope you are learning.")
# Output: Hi Eric Robbie, I hope you are learning.

# Có thể tính toán bên trong {}
age = 25
print(f"Next year {first_name} will be {age + 1} years old.")
# Output: Next year Eric will be 26 years old.

# Định dạng số
price = 59.999
print(f"Price: ${price:.2f}")           # Output: Price: $60.00
print('------------------------f-strings---------------------------------')