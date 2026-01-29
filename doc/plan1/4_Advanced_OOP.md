# 4. Lập trình hướng đối tượng nâng cao (Advanced OOP)

OOP trong Python không chỉ là tạo Class và Object. Để viết code "Pro", bạn cần hiểu sâu về Magic Methods, Decorators trong Class và tư duy Abstraction (Trừu tượng hóa). Đây là nền tảng để hiểu cách các thư viện lớn như SQLAlchemy hay Tortoise ORM hoạt động.

---

## 4.1. Class Variables vs Instance Variables

Phân biệt sai hai cái này sẽ dẫn đến các lỗi logic rất khó tìm.

```python
class Employee:
    # Class Variable: Dùng chung cho TẤT CẢ nhân viên
    company_name = "Tech Corp"
    
    def __init__(self, name):
        # Instance Variable: Riêng biệt cho TỪNG nhân viên
        self.name = name

emp1 = Employee("Alice")
emp2 = Employee("Bob")

print(emp1.company_name) # Tech Corp
print(emp2.company_name) # Tech Corp

# Đổi tên công ty toàn cục
Employee.company_name = "Future Inc"
print(emp1.company_name) # Future Inc (Cả 2 đều thay đổi theo)

# NHƯNG COI CHỪNG:
emp1.company_name = "Solo Company" 
# Dòng trên TẠO RA một instance variable mới tên company_name đè lên class variable CHỈ CHO emp1
print(emp1.company_name) # Solo Company
print(emp2.company_name) # Future Inc (Vẫn giữ giá trị chung)
```

---

## 4.2. @classmethod vs @staticmethod

Thường dùng khi viết Factory Pattern (Tạo object theo nhiều cách khác nhau).

```python
import datetime

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 1. Class Method: Nhận class (cls) làm tham số đầu tiên, không cần self.
    # Thường dùng làm "Constructor thay thế".
    @classmethod
    def from_birth_year(cls, name, birth_year):
        current_year = datetime.date.today().year
        age = current_year - birth_year
        return cls(name, age) # Tương đương Person(name, age)

    # 2. Static Method: Không nhận cls lẫn self. Nó chỉ là hàm bình thường nằm trong class cho gọn.
    @staticmethod
    def is_adult(age):
        return age >= 18

p1 = Person("John", 25)
p2 = Person.from_birth_year("Doe", 2000) # Tạo object từ năm sinh

print(p2.age) # Tự tính ra tuổi
print(Person.is_adult(20)) # True
```

---

## 4.3. Magic Methods (Dunder Methods - Double Underscore)

Đây là cách Python cho phép bạn định nghĩa hành vi của Object với các toán tử `+`, `-`, `len()`, `str()`.

### `__str__` vs `__repr__`
*   `__str__`: Cho người dùng cuối đọc (User friendly).
*   `__repr__`: Cho lập trình viên debug (Rõ ràng, nên bao gồm cách tái tạo object).

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    # Cho phép cộng 2 vector: v1 + v2
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    # Cho phép so sánh bằng: v1 == v2
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v3 = v1 + v2 # Gọi hàm __add__ ngầm bên dưới

print(v3) # Output: Vector(4, 6)
print(v1 == Vector(1, 2)) # True
```

---

## 4.4. Encapsulation & Property Decorators

Python không có `private` thực sự như Java. Nhưng chúng ta dùng quy ước `_` và `@property` để kiểm soát truy cập.

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance # Dấu _: Ý bảo "Đừng sửa trực tiếp biến này bên ngoài"

    @property
    def balance(self):
        """Getter: Cho phép đọc số dư"""
        return self._balance

    @balance.setter
    def balance(self, value):
        """Setter: Logic kiểm tra khi gán giá trị mới"""
        if value < 0:
            raise ValueError("Số dư không thể âm!")
        print(f"Update balance: {value}")
        self._balance = value

acc = BankAccount(100)
print(acc.balance) # Gọi getter -> 100

acc.balance = 50   # Gọi setter -> Update balance: 50
# acc.balance = -10 # Lỗi: ValueError
```

---

## 4.5. Dataclasses (Python 3.7+)

Nếu Class chỉ dùng để chứa dữ liệu (Data Container), đừng viết `__init__`, `__repr__`, `__eq__` mỏi tay. Hãy dùng `dataclass`.

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    email: str
    active: bool = True # Giá trị mặc định

# Tự động sinh ra __init__, __repr__, __eq__ cho mình
u1 = User(1, "admin", "admin@test.com")
u2 = User(1, "admin", "admin@test.com")

print(u1) # Output đẹp: User(id=1, username='admin', email='admin@test.com', active=True)
print(u1 == u2) # True (Tự so sánh nội dung thay vì so sánh địa chỉ bộ nhớ)
```

---

## 4.6. Abstract Base Classes (ABC)

Quy định "luật chơi" cho các class con. Class con BẮT BUỘC phải thực thi các phương thức trừu tượng.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    # Nếu quên implement speak(), Class Cat sẽ báo lỗi ngay khi khởi tạo
    def speak(self): 
        return "Meow!"

# a = Animal() # Lỗi: Không thể khởi tạo Abstract Class
d = Dog()
print(d.speak())
```

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **Smart Phone Class**:
    *   Tạo class `Phone` có attribute `_battery` (private).
    *   Dùng `@property` để cho phép đọc pin.
    *   Dùng `@battery.setter` để đảm bảo pin chỉ nhận giá trị 0-100.
2.  **Vector Math**:
    *   Nâng cấp class `Vector` ở ví dụ trên.
    *   Thêm `__sub__` (trừ), `__mul__` (nhân với số scalar), và `__len__` (trả về độ dài vector - gợi ý: căn bậc 2 của x^2 + y^2).
3.  **Employee Dataclass**:
    *   Dùng `dataclass` tạo `Employee` (id, name, salary).
    *   Tạo list chứa 5 nhân viên.
    *   Tìm nhân viên có lương cao nhất (Dùng `max(list, key=...)` kết hợp kiến thức bài trước).

*Tip: `Dataclasses` được dùng rất nhiều trong FASTAPI để định nghĩa các DTO (Data Transfer Object) nội bộ, hãy làm quen với nó!*
