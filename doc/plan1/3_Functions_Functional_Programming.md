# 3. Hàm & Lập trình hàm (Functions & Functional Programming)

Đây là bước chuyển mình từ "viết mã" sang "thiết kế mã". Hàm không chỉ để chạy code, mà để tái sử dụng, cô lập logic và tạo ra sự linh hoạt. Đặc biệt, **Decorators** và **Generators** là hai khái niệm buộc phải nắm vững để làm việc với FastAPI.

---

## 3.1. Function Basics (Cơ bản về Hàm)

### 1. `*args` và `**kwargs`
Làm sao viết một hàm nhận vào số lượng tham số tùy ý? (Ví dụ hàm `print()` nhận bao nhiêu biến cũng được).

*   `*args`: Nhận danh sách các tham số vị trí (vào tuple).
*   `**kwargs`: Nhận danh sách các tham số có tên (vào dict).

```python
def log_data(level, *messages, **details):
    print(f"[{level}] Info: {messages}")
    print(f"Details: {details}")

# Gọi hàm
log_data("INFO", "Server started", "Port 8000", id=123, status="OK")

# Output:
# [INFO] Info: ('Server started', 'Port 8000')
# Details: {'id': 123, 'status': 'OK'}
```

### 2. "Cái bẫy" Default Mutable Arguments (Cực nguy hiểm)
Sai lầm phổ biến nhất của người mới (và cả senior).
**Tuyệt đối KHÔNG** dùng List hoặc Dict làm giá trị mặc định cho tham số.

```python
# SAI LẦM:
def add_item(item, box=[]): # List [] được tạo ra 1 lần duy nhất khi định nghĩa hàm!
    box.append(item)
    return box

print(add_item("A")) # ['A']
print(add_item("B")) # ['A', 'B'] -> Ủa? Sao B lại chui vào box cũ?

# CÁCH ĐÚNG:
def add_item_safe(item, box=None):
    if box is None:
        box = [] # Tạo list mới mỗi khi gọi hàm
    box.append(item)
    return box
```

---

## 3.2. Scope & Namespaces (Phạm vi biến)

Quy tắc **LEGB**: Python tìm tên biến theo thứ tự:
1.  **L**ocal (Trong hàm)
2.  **E**nclosing (Hàm bao ngoài hàm - Closures)
3.  **G**lobal (Toàn cục module)
4.  **B**uilt-in (Có sẵn như `len`, `str`)

**Keyword `global` và `nonlocal`**:
*   `global x`: Báo rằng tôi muốn sửa biến ở Global scope.
*   `nonlocal x`: Báo rằng tôi muốn sửa biến ở hàm cha (Enclosing) - dùng trong Decorators.

---

## 3.3. Functional Tools (Công cụ lập trình hàm)

### 1. Lambda Functions
Hàm "mì ăn liền", viết trên 1 dòng. Thường dùng khi cần truyền hàm vào hàm khác (`sort`, `map`).

```python
data = [{"name": "A", "age": 20}, {"name": "B", "age": 15}]
# Sort theo age
data.sort(key=lambda x: x["age"]) 
```

### 2. Map, Filter
*   `map(func, list)`: Áp dụng hàm lên từng phần tử.
*   `filter(func, list)`: Lọc giữ lại phần tử thỏa mãn điều kiện.

```python
nums = [1, 2, 3, 4]
# Map: Nhân đôi
doubled = list(map(lambda x: x*2, nums)) # [2, 4, 6, 8]

# Filter: Lấy số chẵn
evens = list(filter(lambda x: x%2 == 0, nums)) # [2, 4]
```

---

## 3.4. Decorators - "Ma thuật" của Python (Cốt lõi FastAPI)

FastAPI dùng decorators `(@app.get)` khắp nơi. Bản chất Decorator là **Higher-Order Function**: Nhận vào 1 hàm, trả về 1 hàm mới mạnh mẽ hơn.

### Cấu trúc chuẩn của một Decorator
```python
import functools
import time

def timer_decorator(func):
    # Dùng wraps để giữ lại tên và docstring của hàm gốc (quan trọng!)
    @functools.wraps(func) 
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Chạy hàm gốc
        result = func(*args, **kwargs)
        
        end_time = time.time()
        print(f"Hàm {func.__name__} chạy mất: {end_time - start_time:.4f}s")
        return result
    
    return wrapper

# Cách dùng:
@timer_decorator
def heavy_calculation():
    time.sleep(1)
    print("Done logic!")

heavy_calculation()
# Output:
# Done logic!
# Hàm heavy_calculation chạy mất: 1.0012s
```

---

## 3.5. Generators & Yield (Xử lý dữ liệu lớn)

List lưu tất cả vào RAM. Generator thì không, nó tạo ra từng giá trị khi cần (Lazy evaluation).

### Ví dụ: Đọc file siêu lớn (10GB)
Nếu dùng `read()` thường, RAM sẽ nổ. Dùng Generator để đọc từng dòng.

```python
def read_large_file(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield line.strip() # Trả về 1 dòng rồi tạm dừng, chờ gọi tiếp

# Sử dụng
# Hàm chưa chạy ngay, nó trả về 1 generator object
log_lines = read_large_file("huge_log.txt") 

# Chỉ khi loop, code mới chạy từng dòng
for line in log_lines:
    if "ERROR" in line:
        print("Found error:", line)
        break # Dừng ngay lập tức, không đọc hết file -> Hiệu năng cực cao
```

### Generator Expression
Giống List Comprehension nhưng dùng ngoặc tròn `()`. Tiết kiệm RAM.
```python
# List Comp: Tạo mảng 1 triệu số -> Ngốn RAM ngay lập tức
squares_list = [n**2 for n in range(1000000)] 

# Generator Exp: Không tốn RAM, chỉ tốn công thức
squares_gen = (n**2 for n in range(1000000))
```

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **Viết Decorator `retry`**:
    *   Tạo decorator `@retry(times=3)` nhận vào tham số số lần thử.
    *   Nếu hàm bên dưới ném Exception, nó sẽ tự động chạy lại tối đa `times` lần trước khi thực sự báo lỗi. (Rất hay dùng khi gọi API chập chờn).
2.  **Generator Sequence**:
    *   Viết hàm `my_range(start, end, step)` sử dụng `yield`, hoạt động y hệt hàm `range()` có sẵn của Python.
3.  **Lambda Sort**:
    *   Cho list tuples: `students = [('Tuan', 'B', 12), ('An', 'A', 15), ('Binh', 'A', 10)]`. (Tên, Xếp loại, Tuổi).
    *   Sort list này ưu tiên theo Xếp loại (A->Z), nếu trùng xếp loại thì sort theo Tuổi (tăng dần).

*Tip: Hiểu được phần Decorator là bạn đã nắm được 50% "phép thuật" của các Framework Python rồi đó!*
