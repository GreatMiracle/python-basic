# 2. Cấu trúc dữ liệu & Giải thuật cơ bản (Data Structures)

Cấu trúc dữ liệu là xương sống của mọi chương trình. Chọn đúng cấu trúc dữ liệu giúp code chạy nhanh như tên lửa, chọn sai code sẽ "rùa bò" khi dữ liệu lớn lên. Ở phần này, ta không chỉ học cách "khai báo biến" mà học **cơ chế bên trong (Internal mechanics)** của chúng.

---

## 2.1. String Manipulation (Xử lý chuỗi nâng cao)

String trong Python là **Immutable** (không thể thay đổi). Mọi phép cộng chuỗi đều tạo ra một chuỗi mới trong bộ nhớ.

### 1. F-strings (Formatted String Literals) - Kỷ nguyên mới
Quên ngay `%s` hay `.format()` đi. Từ Python 3.6+, hãy dùng f-string. Nhanh hơn và dễ đọc hơn.

```python
name = "Anti"
score = 95.5123

# Cơ bản
print(f"Hello {name}, your score is {score}")

# Format số thực (2 số thập phân)
print(f"Score: {score:.2f}")  # Output: Score: 95.51

# Debug nhanh (cực hay): In cả tên biến và giá trị
print(f"{name=}, {score=}")   # Output: name='Anti', score=95.5123
```

### 2. Slicing - Cắt chuỗi thần thánh
Cú pháp: `string[start:stop:step]`

```python
s = "PythonProfessional"

print(s[0:6])   # 'Python' (Lấy từ 0 đến trước 6)
print(s[:6])    # 'Python' (Bỏ start mặc định là 0)
print(s[6:])    # 'Professional' (Lấy từ 6 đến hết)
print(s[-1])    # 'l' (Lấy ký tự cuối cùng)
print(s[::-1])  # 'lanoisseforPnohtyP' (Đảo ngược chuỗi - step là âm)
print(s[::2])   # 'PtoPofsinl' (Lấy cách quãng 2 ký tự)
```

### 3. Encoding vs Decoding
Khi làm việc với mạng (API, file), dữ liệu là `bytes`, không phải `str`.
*   **Encode**: Biến `str` (dễ đọc) -> `bytes` (máy tính lưu trữ).
*   **Decode**: Biến `bytes` -> `str`.

```python
text = "Xin chào"
# String -> Bytes (để gửi qua mạng)
data_bytes = text.encode("utf-8")
print(data_bytes)  # b'Xin ch\xc3\xa0o'

# Bytes -> String (để hiển thị)
decoded_text = data_bytes.decode("utf-8")
```

---

## 2.2. List (Mảng động - Dynamic Array)

**Bản chất**: List trong Python là một mảng các con trỏ (pointers). Nó có thể chứa hỗn hợp các kiểu dữ liệu.

### 1. Cơ chế bộ nhớ (Dynamic Resizing)
Khi bạn `append` phần tử vào list đầy, Python phải:
1.  Cấp phát vùng nhớ mới to hơn (thường gấp đôi).
2.  Copy dữ liệu cũ sang.
3.  Thêm phần tử mới.
-> **Lời khuyên**: List rất mạnh, nhưng nếu dữ liệu cực lớn và toàn số, hãy dùng `array` hoặc thư viện `NumPy`.

### 2. List Comprehension
Cách tạo list "Pythonic" nhất - ngắn gọn và chạy nhanh hơn loop `for` thông thường.

```python
numbers = [1, 2, 3, 4, 5]

# Cách truyền thống (Dài dòng)
squares = []
for n in numbers:
    if n % 2 == 0:
        squares.append(n * n)

# Cách Pro (List Comprehension)
# [expression for item in iterable if condition]
squares_pro = [n * n for n in numbers if n % 2 == 0]
# Output: [4, 16]
```

### 3. Sorting: `sort()` vs `sorted()`
*   `list.sort()`: Sắp xếp **tại chỗ** (Sửa đổi list gốc). Trả về `None`.
*   `sorted(list)`: Tạo ra **list mới** đã sắp xếp. List gốc giữ nguyên.

```python
data = [{"name": "A", "age": 25}, {"name": "B", "age": 20}]

# Sort theo key tùy chỉnh (cực quan trọng khi làm backend)
data.sort(key=lambda x: x["age"])
# Kết quả: B đứng trước A vì age 20 < 25
```

---

## 2.3. Dictionary (Hash Map) - Cấu trúc quyền lực nhất

Backend Development = Xử lý Dictionary. JSON trả về từ API chính là Dictionary.

### 1. Hash Map hoạt động thế nào?
Key của dict phải là **Immutable** (Hashable) như số, chuỗi, tuple. List không thể làm key.
Tốc độ truy xuất của Dict là **O(1)** - Tức là dù Dict có 1 triệu phần tử, tìm 1 phần tử vẫn tốn thời gian như tìm trong Dict có 10 phần tử.

### 2. Các method cần biết
```python
user = {"id": 1, "name": "Admin", "role": "SuperUser"}

# 1. Lấy giá trị an toàn (Tránh lỗi KeyError)
# print(user["email"]) -> Error crash app!
email = user.get("email", "no-email@test.com") # Trả về default nếu không thấy

# 2. setdefault: Lấy giá trị, nếu chưa có thì gán default luôn
tags = {}
# Nếu key 'python' chưa có, gán nó là [], sau đó append
tags.setdefault("python", []).append("article1")

# 3. Merging (Python 3.9+)
default_settings = {"theme": "light", "notifications": True}
user_settings = {"theme": "dark"}

# Hợp nhất: user đè lên default
config = default_settings | user_settings
# Output: {'theme': 'dark', 'notifications': True}
```

### 3. Loop qua Dict hiệu quả
```python
# Cách tồi:
for k in user:
    val = user[k] # Truy xuất thêm 1 lần nữa -> chậm

# Cách đúng:
for k, v in user.items():
    print(f"{k}: {v}")
```

---

## 2.4. Set & Tuple

### Set (Tập hợp) - Khử trùng lặp
Dùng Set để tìm kiếm phần tử nhanh O(1) hoặc loại bỏ dữ liệu trùng.
```python
emails = ["a@a.com", "b@b.com", "a@a.com"]
unique_emails = set(emails) # {'a@a.com', 'b@b.com'}

# Phép toán tập hợp (Rất hữu ích khi phân quyền User)
admin_perms = {"read", "write", "delete"}
user_perms = {"read"}

# Kiểm tra user thiếu quyền gì so với admin?
missing = admin_perms - user_perms # {'write', 'delete'}
```

### Tuple - Dữ liệu bất biến
Giống List nhưng không sửa được. Nhanh hơn List và chiếm ít RAM hơn.
**Trick Unpacking (Giải nén):**
```python
coordinates = (10, 20)
x, y = coordinates # x=10, y=20

# Hoán đổi giá trị không cần biến tạm
a, b = 5, 10
a, b = b, a 
```

---

## 2.5. Advanced Collections (`collections` Module)

Thư viện chuẩn, import là dùng, giúp code chuyên nghiệp hơn hẳn.

### 1. `Counter` - Đếm tần suất
```python
from collections import Counter

logs = ["error", "info", "error", "warning", "error"]
stats = Counter(logs)
print(stats)
# Output: Counter({'error': 3, 'info': 1, 'warning': 1})

print(stats.most_common(1)) # [('error', 3)]
```

### 2. `defaultdict` - Dict không bao giờ lỗi key
```python
from collections import defaultdict

# Tự động tạo int (0) nếu key chưa có
scores = defaultdict(int) 
scores["player1"] += 10 # Không lỗi dù "player1" chưa tồn tại trước đó!
```

### 3. `namedtuple` - Tuple có tên (Tiền thân của Dataclass)
Dùng khi bạn muốn trả về một object nhẹ nhàng, không cần viết class phức tạp.
```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p1 = Point(10, 20)

print(p1.x) # 10 (Dễ đọc hơn p1[0])
```

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **List Comprehension**: Tạo một list các số chẵn từ 0 đến 100, sau đó bình phương chúng lên. Chỉ dùng 1 dòng code.
2.  **Dictionary Processing**:
    *   Tạo một list chứa các dicts: `users = [{"name": "A", "score": 8}, {"name": "B", "score": 5}, {"name": "C", "score": 9}]`.
    *   Dùng `sort` để sắp xếp users theo score giảm dần.
3.  **Unique Counter**: Viết một đoạn script nhập vào một đoạn văn bản dài, đếm xem mỗi từ xuất hiện bao nhiêu lần, và in ra top 3 từ xuất hiện nhiều nhất (Gợi ý: Dùng `split()`, `Counter`).

*Tip: Hãy thử code ngay trong file `practice_datastruct.py` để "ngấm" nhé!*
