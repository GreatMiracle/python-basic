# 5. Modern Python & Type Hinting (Nền tảng của FastAPI)

Trước đây Python là ngôn ngữ "động" (Dynamic typing) - bạn không cần khai báo kiểu của biến. Nhưng trong thế giới Enterprise và Backend hiện đại (nhất là với **FastAPI**), **Type Hinting** là bắt buộc. Nó giúp code tường minh, IDE gợi ý thông minh, và quan trọng nhất: **FastAPI dùng nó để tự động Validate dữ liệu**.

---

## 5.1. Cơ bản về Type Hinting

Cú pháp: `variable: type = value`.
Lưu ý: Python runtime mặc định **KHÔNG** bắt lỗi sai kiểu (nó chỉ là "lời gợi ý"). Nhưng các tool như `mypy` hay FastAPI sẽ dùng nó.

### Biến đơn giản
```python
# Cách cũ
age = 25
name = "Anti"

# Cách Modern (Rõ ràng)
age: int = 25
name: str = "Anti"
is_active: bool = True
rating: float = 4.5
```

### Hàm (Parameters & Return Type)
```python
# Hàm này nhận tên (chuỗi) và trả về lời chào (chuỗi)
def greet(name: str) -> str:
    return f"Hello, {name}"

# IDE sẽ báo vàng nếu bạn gọi: greet(123)
```

---

## 5.2. Các kiểu dữ liệu phức tạp (`List`, `Dict`, `Set`)

Trước Python 3.9, bạn phải import từ module `typing`.
Từ Python 3.9+, bạn dùng luôn kiểu có sẵn (built-in).

```python
# --- Python 3.9+ (Nên dùng) ---
numbers: list[int] = [1, 2, 3]
user_info: dict[str, int] = {"id": 1, "age": 30} # Key là str, Value là int
unique_ids: set[int] = {1, 2, 3}
tuple_data: tuple[str, int] = ("A", 1)

# --- Python < 3.9 (Cũ - chỉ nên biết để đọc code cũ) ---
from typing import List, Dict, Set, Tuple
numbers: List[int] = [1, 2, 3]
```

---

## 5.3. Kiểu đặc biệt (Special Types)

Những kiểu này cực kỳ phổ biến trong FastAPI.

### 1. `Optional` (Có thể là None)
Biến `email` có thể là chuỗi, hoặc chưa có (`None`).
```python
from typing import Optional

# Cách 1 (Cũ):
email: Optional[str] = None

# Cách 2 (Python 3.10+ - Dấu gạch đứng):
email: str | None = None
```

### 2. `Union` (Nhiều kiểu khác nhau)
Biến `user_id` có thể là số nguyên (1) hoặc chuỗi UUID ("abc-xyz").
```python
from typing import Union

def get_item(item_id: Union[int, str]):
    print(f"Item ID: {item_id}")

# Python 3.10+ syntax:
def get_item_modern(item_id: int | str):
    pass
```

### 3. `Any` (Chấp nhận tất cả)
Dùng khi bạn thực sự không biết kiểu dữ liệu là gì (hoặc lười). **Hạn chế tối đa dùng cái này**, vì nó làm mất ý nghĩa của Type Hint.
```python
from typing import Any

def print_anything(data: Any):
    print(data)
```

### 4. `Callable` (Truyền hàm vào hàm)
```python
from typing import Callable

# Tham số 'func' là một hàm nhận 2 số int và trả về 1 số int
def calculator(a: int, b: int, func: Callable[[int, int], int]):
    return func(a, b)
```

---

## 5.4. Pydantic - Dữ liệu hướng đối tượng (Data Validation)

FastAPI "đứng trên vai người khổng lồ" Pydantic. Đây là thư viện dùng Type Hint để validate dữ liệu THẬT.

### Ví dụ kinh điển:
Không dùng Pydantic, bạn phải if/else mệt mỏi:
```python
# Code cũ thủ công
data = {"name": "Alice", "age": "INVALID"}
if "age" in data and isinstance(data["age"], int):
    # logic...
else:
    # raise error...
```

Dùng **Pydantic** (FastAPI style):
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str 
    age: int
    email: str | None = None # Optional

# Dữ liệu đầu vào (từ JSON request chẳng hạn)
external_data = {
    "id": "123", # Pydantic tự ép kiểu chuỗi "123" thành số 123
    "name": "Alice",
    "age": 30
    # email thiếu -> Tự gán None
}

# Validate
user = User(**external_data) 
print(user.id) # 123 (kiểu int)
print(user.dict()) # {'id': 123, 'name': 'Alice', 'age': 30, 'email': None}
```
*Nếu dữ liệu sai (ví dụ age="abc"), Pydantic sẽ ném lỗi chi tiết ngay lập tức!*

---

## 5.5. Static Analysis với `mypy`

Type Hint chỉ là gợi ý. Để bắt lỗi TRƯỚC khi chạy code, ta dùng tool `mypy`.
**Cài đặt**: `pip install mypy`

**Ví dụ code lỗi (`bug.py`):**
```python
def add(a: int, b: int) -> int:
    return a + b

add("1", 2) # Code chạy vẫn lỗi Runtime, nhưng IDE báo vàng
```

**Chạy lệnh**:
```bash
mypy bug.py
```
**Kết quả**:
`bug.py:4: error: Argument 1 to "add" has incompatible type "str"; expected "int"`

-> Nhờ `mypy`, bạn sửa được lỗi ngay khi viết code, không đợi đến lúc chạy mới crash app.

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **Refactor Code cũ**:
    *   Lấy một bài tập ở phần Function (ví dụ hàm tính toán), thêm Type Hint đầy đủ cho tham số và giá trị trả về.
2.  **Pydantic Model**:
    *   Tạo class `Product` kế thừa `BaseModel`.
    *   Có các trường: `name` (str), `price` (float), `tags` (list[str]), `is_available` (bool, default=True).
    *   Thử khởi tạo với dictionary dữ liệu đúng và dictionary dữ liệu sai để xem Pydantic báo lỗi thế nào.
3.  **Hàm tìm kiếm**:
    *   Viết hàm `find_user(users: list[dict], user_id: int) -> dict | None`.
    *   Hàm trả về user dict nếu tìm thấy, hoặc `None` nếu không thấy. Code phải có type hint chuẩn Python 3.10+.

*Tip: Khi làm quen với Type Hint, ban đầu bạn sẽ thấy hơi "rườm rà", nhưng khi project lớn lên, bạn sẽ cảm ơn nó vì đã cứu bạn khỏi hàng ngàn lỗi ngớ ngẩn!*
