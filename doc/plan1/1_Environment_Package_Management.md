# 1. Môi trường & Quản lý Gói (Environment & Package Management)

Bài học đầu tiên và quan trọng nhất không phải là viết code, mà là **quản lý nơi code chạy**. Nếu không làm chủ được môi trường, bạn sẽ sớm gặp cơn ác mộng "Dependency Hell" (địa ngục thư viện) - nơi code chạy trên máy tôi nhưng không chạy trên máy bạn, hoặc sửa dự án A làm hỏng dự án B.

---

## 1.1. Virtual Environments (Môi trường ảo)

### Tại sao CẦN PHẢI DÙNG?
Tưởng tượng bạn có 2 dự án:
*   **Dự án A** (Web cũ): Dùng thư viện `Django 2.0`.
*   **Dự án B** (Web mới): Dùng thư viện `Django 5.0`.

Nếu cài trực tiếp vào máy (Global Python), bạn chỉ cài được một phiên bản. Cài cái này đè mất cái kia -> Một dự án sẽ chết.
**Giải pháp**: Mỗi dự án có một "hộp kín" riêng chứa Python và các thư viện của riêng nó. Đó là Virtual Environment.

### Cách sử dụng `venv` (Standard Library)
Đây là công cụ có sẵn trong Python, luôn phải biết dùng.

**1. Tạo môi trường ảo**
Mở terminal tại thư mục gốc dự án:
```bash
# Cấu trúc: python -m venv <tên_thư_mục_ảo>
# Thường đặt tên là .venv hoặc venv
python -m venv .venv
```

**2. Kích hoạt môi trường (Activate)**
Sau khi tạo, bạn phải "bước vào" môi trường đó.
*   **Windows (Command Prompt / Powershell):**
    ```powershell
    # Windows
    .\.venv\Scripts\activate
    ```
    *Dấu hiệu thành công*: Đầu dòng lệnh sẽ hiện `(.venv) C:\path\to\project>`.

*   **Linux / macOS:**
    ```bash
    source .venv/bin/activate
    ```

**3. Thoát môi trường (Deactivate)**
Khi làm xong, muốn quay về môi trường gốc:
```bash
deactivate
```

---

## 1.2. PIP - Trình quản lý gói (Python Package Installer)

Khi đã ở trong môi trường ảo, bạn dùng `pip` để tải thư viện từ kho [PyPI](https://pypi.org/).

### Các lệnh cốt lõi

| Lệnh | Ý nghĩa | Ví dụ |
| :--- | :--- | :--- |
| `pip install <tên>` | Cài bản mới nhất | `pip install requests` |
| `pip install <tên>==<version>` | Cài đúng phiên bản | `pip install numpy==1.21.0` |
| `pip uninstall <tên>` | Gỡ cài đặt | `pip uninstall pandas` |
| `pip list` | Xem các gói đã cài | `pip list` |
| `pip show <tên>` | Xem thông tin chi tiết gói | `pip show fastapi` |

### Quản lý Dependencies (`requirements.txt`)
Để người khác chạy được code của bạn, họ cần biết phải cài những gì.
**1. Xuất danh sách gói đã cài:**
```bash
# Lưu toàn bộ thư viện hiện tại vào file
pip freeze > requirements.txt
```
*Nội dung file `requirements.txt` sẽ trông như thế này:*
```text
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.6.0
```

**2. Cài đặt từ danh sách (cho người mới tham gia dự án):**
```bash
pip install -r requirements.txt
```

---

## 1.3. Hệ thống Module & Import (Module System)

Đây là phần newbie hay rối nhất. Hiểu sai phần này dẫn đến lỗi kinh điển `ModuleNotFoundError`.

### Module vs Package
*   **Module**: Là *một file* `.py` bất kỳ.
*   **Package**: Là *một thư mục* chứa các modules và file đặc biệt `__init__.py`.

### Cơ chế tìm kiếm (`sys.path`)
Khi bạn gõ `import abc`, Python tìm file `abc.py` ở đâu? Nó quét lần lượt trong danh sách đường dẫn `sys.path`:
1.  Thư mục hiện tại đang chạy lệnh script.
2.  Biến môi trường `PYTHONPATH`.
3.  Thư mục cài đặt Python mặc định.

**Ví dụ soi `sys.path`:**
```python
import sys
# In ra danh sách các nơi Python sẽ lục lọi để tìm thư viện
for path in sys.path:
    print(path)
```

### Absolute Import vs Relative Import
Giả sử cấu trúc dự án:
```text
project/
├── main.py
└── mypackage/
    ├── __init__.py
    ├── utils.py
    └── database.py
```

**1. Absolute Import (Khuyên dùng - Rõ ràng)**
Luôn tính từ thư mục gốc của dự án.
```python
# Trong file main.py hoặc database.py đều viết được
from mypackage import utils
from mypackage.utils import connect_db
```
*Ưu điểm*: Rõ ràng, dễ debug, không phụ thuộc vị trí file hiện tại.

**2. Relative Import (Dấu chấm)**
Chỉ dùng trong nội bộ package, tính từ vị trí file hiện tại.
*   `.`: Cùng thư mục.
*   `..`: Thư mục cha.

```python
# Trong file database.py
from . import utils  # Import utils.py cùng thư mục
from .utils import help_func
```
*Nhược điểm*: Khó đọc, dễ lỗi nếu chạy file script trực tiếp (do `__name__` thay đổi).

### Vai trò của `__init__.py`
File này báo cho Python biết: "Thư mục chứa tôi là một Package, hãy treat nó như một đơn vị import".
*   Có thể để trống (thường gặp).
*   Có thể dùng để gom gọn imports.

**Ví dụ "Gom gọn" với `__init__.py`**:
*Trong `mypackage/database.py`:*
```python
class Database:
    pass
```
*Trong `mypackage/__init__.py`:*
```python
# Expose class Database ra ngoài package
from .database import Database
```
*Lúc dùng (Clean hơn):*
```python
# Thay vì viết dài:
from mypackage.database import Database
# Chỉ cần viết:
from mypackage import Database
```

---

## 1.4. The Main Guard (`if __name__ == "__main__":`)

Tại sao file Python nào cũng thấy dòng này cuối cùng?

**Vấn đề**: Khi bạn `import` một file, Python sẽ **CHẠY TOÀN BỘ** code trong file đó ngay lập tức (từ trên xuống dưới).

**Ví dụ thảm họa**:
File `lib.py`:
```python
def phep_cong(a, b):
    return a + b

# Code test nhanh của dev
print("Kết quả test:", phep_cong(1, 2))
```

File `main.py`:
```python
import lib
# Vừa import xong, màn hình in luôn dòng "Kết quả test: 3" -> Vô duyên!
```

**Giải pháp**: Dùng `if __name__ == "__main__":`
Biến `__name__` là biến đặc biệt:
*   Nếu file được chạy trực tiếp (`python lib.py`) -> `__name__` bằng `"__main__"`.
*   Nếu file bị import (`import lib`) -> `__name__` bằng `"lib"`.

Sửa lại `lib.py`:
```python
def phep_cong(a, b):
    return a + b

# Chỉ chạy đoạn dưới nếu file này được chạy trực tiếp
if __name__ == "__main__":
    print("Kết quả test:", phep_cong(1, 2))
```

---

## BÀI TẬP THỰC HÀNH (Action Items)

Để thực sự hiểu, bạn hãy làm ngay các bước sau trên máy:

1.  **Setup dự án**:
    *   Tạo thư mục `python-practice`.
    *   Mở terminal, tạo môi trường ảo `.venv`.
    *   Activate môi trường ảo.
    *   Tạo file `.gitignore` và thêm dòng `.venv/` vào đó (để không bao giờ commit môi trường ảo lên git).

2.  **Cài gói và Xuất file**:
    *   Chạy `pip install requests colorama`.
    *   Chạy `pip freeze > requirements.txt`.
    *   Mở file text xem kết quả.

3.  **Thử nghiệm Import**:
    *   Tạo file `my_script.py`.
    *   Import `colorama` vừa cài để in chữ màu xanh.
    *   Viết hàm `main()` và dùng `if __name__ == "__main__":` để gọi nó.

*Ghi chú: Khi nào làm xong báo tôi, chúng ta sẽ sang phần 2 về Cấu trúc dữ liệu!*
