# 6. Xử lý Lỗi & I/O (Error Handling & Input/Output)

Một ứng dụng chuyên nghiệp không phải là ứng dụng không bao giờ lỗi, mà là ứng dụng biết cách **xử lý lỗi duyên dáng** (Graceful handling) thay vì crash thẳng mặt người dùng. Ngoài ra, việc đọc/ghi file và tương tác hệ điều hành cũng là kỹ năng sống còn.

---

## 6.1. Exception Handling (Xử lý Ngoại lệ)

### Cấu trúc `try...except...else...finally`
Chúng ta không chỉ xài `try-except` mà còn có 2 khối quyền lực khác ít người biết.

```python
try:
    # Code có thể gây lỗi
    file = open("data.txt", "r")
    content = int(file.read()) # Lỗi nếu file không chứa số

except FileNotFoundError:
    # Chạy khi không thấy file
    print("Lỗi: File không tồn tại!")
    
except ValueError as e:
    # Chạy khi ép kiểu lỗi
    print(f"Lỗi dữ liệu: {e}")

except Exception:
    # Chạy cho tất cả lỗi còn lại (HẠN CHẾ DÙNG)
    print("Lỗi không xác định đã xảy ra.")

else:
    # Chạy khi KHÔNG CÓ lỗi nào xảy ra trong khối try
    print("Đọc file thành công!")
    print("Dữ liệu là:", content)

finally:
    # LUÔN LUÔN CHẠY dù có lỗi hay không
    # Thường dùng để dọn dẹp (đóng file, ngắt kết nối DB)
    print("Đang đóng file...")
    if 'file' in locals() and not file.closed:
        file.close()
```

### 3 Quy tắc vàng khi bắt lỗi
1.  **Cụ thể tốt hơn chung chung**: Bắt `ValueError`, `KeyError` thay vì bắt `Exception`.
2.  **Đừng nuốt chửng lỗi (Swallowing exceptions)**:
    ```python
    # TỒI TỆ:Code sai nhưng không ai biết
    except Exception:
        pass 
    ```
3.  **Fail Fast**: Nếu lỗi nghiêm trọng (mất kết nối DB), hãy để nó crash hoặc raise lỗi lên trên, đừng cố chạy tiếp.

### Custom Exceptions (Tự tạo lỗi nghiệp vụ)
Trong FastAPI, ta thường tạo Exception riêng để trả về mã lỗi HTTP đẹp.
```python
class InsufficientFundsError(Exception):
    """Lỗi khi rút quá số dư"""
    def __init__(self, current, amount):
        super().__init__(f"Không đủ tiền! Có: {current}, Rút: {amount}")

# Sử dụng
tk_du = 100
rut = 500
if rut > tk_du:
    raise InsufficientFundsError(tk_du, rut)
```

---

## 6.2. Context Managers (`with` statement)

Bạn có để ý đoạn code `finally` bên trên để đóng file quá cồng kềnh không? Context Manager sinh ra để giải quyết việc đó tự động.

### Dùng sẵn (Built-in)
```python
# Tự động đóng file ngay cả khi có lỗi xảy ra
with open("log.txt", "a") as f:
    f.write("Log line 1\n")
# Ra khỏi khối with -> File tự đóng.
```

### Tự viết Context Manager
Dùng decorator `@contextmanager` là cách nhanh nhất.
```python
from contextlib import contextmanager

@contextmanager
def my_timer(label):
    import time
    start = time.time()
    try:
        yield # Code trong khối wit sẽ chạy ở đây
    finally:
        end = time.time()
        print(f"{label}: {end - start}s")

# Sử dụng
with my_timer("Xử lý vòng lặp"):
    sum([i**2 for i in range(1000000)])
# Output: Xử lý vòng lặp: 0.123s
```

---

## 6.3. File I/O & JSON

### Đọc ghi File Text
*   Mode `w`: Ghi mới (xóa hết nội dung cũ).
*   Mode `a`: Ghi nối đuôi (Append).
*   Mode `r`: Chỉ đọc.

### Xử lý JSON (Format giao tiếp chuẩn của API)
```python
import json

data = {
    "name": "Server A",
    "status": "Running",
    "load": 80.5
}

# 1. Dictionary -> JSON String (Serialize)
json_str = json.dumps(data, indent=2) 
print(json_str)

# 2. JSON String -> Dictionary (Deserialize)
parsed_data = json.loads(json_str)

# 3. Ghi thẳng vào file
with open("config.json", "w") as f:
    json.dump(data, f) # dump (không có s) là ghi file
```

---

## 6.4. Path Handling (`pathlib` - Modern way)

Quên module `os.path` cũ kỹ đi. `pathlib` là cách hướng đối tượng để xử lý đường dẫn, chạy tốt trên cả Windows và Linux/Mac.

```python
from pathlib import Path

# Đường dẫn hiện tại
current_dir = Path.cwd()

# Tạo đường dẫn phụ (Dùng toán tử / cực tiện)
log_file = current_dir / "logs" / "app.log" 

# Kiểm tra tồn tại
if not log_file.exists():
    # Tạo thư mục cha nếu chưa có (mkdir -p)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Tạo file trống
    log_file.touch()

# Đọc ghi nhanh (Text)
log_file.write_text("Startup...", encoding="utf-8")
print(log_file.read_text(encoding="utf-8"))

# Lấy thông tin file
print(log_file.name)   # app.log
print(log_file.suffix) # .log
print(log_file.stem)   # app
```

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **File Converter Safe**:
    *   Viết script đọc file `data.txt` (chứa các số, mỗi số 1 dòng).
    *   Tính tổng các số và ghi vào `result.txt`.
    *   Yêu cầu dùng `try-except` để xử lý trường hợp: File không tồn tại, hoặc File chứa dòng không phải số (bỏ qua dòng đó).
2.  **JSON Config Manager**:
    *   Viết class `ConfigManager` dùng `pathlib`.
    *   Hàm `load()` đọc file `config.json`, nếu file không có thì trả về dict mặc định.
    *   Hàm `save(data)` ghi dict vào file `config.json`.
3.  **Timer Context**:
    *   Tự viết lại context manager tính giờ (giống ví dụ trên) nhưng dùng Class (implement `__enter__` và `__exit__`) thay vì dùng decorator.

*Tip: `pathlib` là thư viện tôi thích nhất trong Python 3, nó biến việc xử lý file path từ nỗi đau đầu thành niềm vui!*
