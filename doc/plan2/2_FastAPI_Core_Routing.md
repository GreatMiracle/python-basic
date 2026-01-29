# 2. FastAPI Core & Routing

Chào mừng bạn đến với thế giới của **FastAPI**. Đây là nơi chúng ta biến lý thuyết HTTP thành code chạy thực tế.
FastAPI được thiết kế để: **Nhanh (Hiệu năng cao)**, **Nhanh (Code lẹ)**, và **Ít lỗi**.

---

## 2.1. Hello World và Cài đặt

Trước hết, bạn cần cài đặt thư viện.
```bash
# Cài fastapi và uvicorn (Web Server để chạy app)
pip install fastapi uvicorn
```

Tạo file `main.py`:
```python
from fastapi import FastAPI

# Khởi tạo ứng dụng
app = FastAPI()

# Routing cơ bản: Khi user vào trang chủ "/"
@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

**Chạy server:**
```bash
# uvicorn <tên_file>:<tên_biến_app> --reload
uvicorn main:app --reload
```
*   `--reload`: Tự động restart server khi bạn sửa code (chỉ dùng lúc dev).
*   Truy cập `http://127.0.0.1:8000` -> Thấy JSON `{"message": "Hello World"}`.
*   Truy cập `http://127.0.0.1:8000/docs` -> Thấy giao diện **Swagger UI** cực xịn.

---

## 2.2. Path Parameters vs Query Parameters

FastAPI phân biệt thông minh 2 loại tham số này.

### Path Parameters (Tham số đường dẫn)
Dùng để định danh tài nguyên cụ thể.
Ví dụ: Lấy user có ID là 5 -> `/users/5`.

```python
@app.get("/items/{item_id}")
def read_item(item_id: int): # Type hint int giúp FastAPI tự validate!
    return {"item_id": item_id, "type": str(type(item_id))}
```
*   Nếu truy cập `/items/5` -> OK.
*   Nếu truy cập `/items/abc` -> Lỗi 422 (FastAPI báo: "value is not a valid integer").

### Query Parameters (Tham số truy vấn)
Dùng để lọc, sắp xếp, tìm kiếm. Nằm sau dấu `?`.
Ví dụ: `/items?skip=0&limit=10`.

```python
# Các tham số KHÔNG có trong path sẽ tự động là Query Param
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```
*   Truy cập `/items/` -> skip=0, limit=10 (mặc định).
*   Truy cập `/items/?limit=50` -> skip=0, limit=50.

---

## 2.3. Request Body & Pydantic (Trái tim của FastAPI)

Để nhận dữ liệu POST (ví dụ tạo user mới), chúng ta dùng **Pydantic Model**.
Đây là tính năng "ăn tiền" nhất của FastAPI: Validate tự động.

```python
from pydantic import BaseModel
from typing import Optional

# 1. Định nghĩa Schema (Khuôn mẫu dữ liệu)
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None # Trường này có thể thiếu

# 2. Sử dụng trong Router
@app.post("/items/")
def create_item(item: Item):
    # item ở đây đã là một object Python xịn, không phải dict
    return {
        "item_name": item.name, 
        "item_price": item.price,
        "tax_price": item.price * 1.1 # Tính toán thoải mái
    }
```
*Client gửi JSON:*
```json
{
    "name": "Laptop",
    "price": 1000
    // is_offer thiếu -> tự thành null
}
```
*Nếu client gửi `price`: "abc" -> FastAPI chặn ngay lập tức.*

---

## 2.4. Response Model (Kiểm soát đầu ra)

Đôi khi DB lấy lên object có chứa `password`, bạn không muốn trả về cho User. Response Model giúp lọc dữ liệu.

```python
class UserCreate(BaseModel):
    username: str
    password: str # Input có pass

class UserOut(BaseModel):
    username: str
    email: str 
    # Output KHÔNG CÓ password

@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate):
    # Giả lập lưu DB và trả về object User đầy đủ
    saved_user = user.dict()
    saved_user["email"] = "user@example.com"
    return saved_user 
    # FastAPI sẽ tự động LỌC bỏ field 'password' trước khi trả về client
```

---

## 2.5. Structuring Project (Tổ chức thư mục)

Đừng viết tất cả vào 1 file `main.py`. Hãy chia nhỏ (Modular) bằng `APIRouter`.

**Cấu trúc thư mục:**
```
my_project/
├── main.py
└── routers/
    ├── __init__.py
    ├── users.py
    └── items.py
```

**File `routers/users.py`:**
```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"], # Để gom nhóm trong Swagger UI
)

@router.get("/")
def get_users():
    return [{"username": "Rick"}, {"username": "Morty"}]
```

**File `main.py`:**
```python
from fastapi import FastAPI
from routers import users, items

app = FastAPI()

# Gắn router con vào app chính
app.include_router(users.router)
app.include_router(items.router)
```

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **Dự án Todo List (Khởi đầu)**:
    *   Tạo file `main.py`.
    *   Tạo Pydantic model `Todo` (id, title, completed).
    *   Tạo biến toàn cục `todos = []` (để lưu tạm trong RAM).
    *   Viết API `POST /todos` để thêm việc.
    *   Viết API `GET /todos` để lấy danh sách.
    *   Viết API `PUT /todos/{id}` để cập nhật trạng thái `completed`.
2.  **Validation Challenge**:
    *   Thêm quy tắc vào model: `title` không được để trống, `id` phải dương.
    *   Thử gửi request sai để xem FastAPI chửi như thế nào.
3.  **Refactor Router**:
    *   Chuyển các api todo sang file `routers/todo.py` và import lại vào main.

*Lời khuyên: Hãy mở `http://127.0.0.1:8000/docs` thường xuyên. Thấy API mình hiện lên đó và nút "Try it out" chạy được là cảm giác rất phê!*
