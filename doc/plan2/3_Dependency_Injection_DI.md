# 3. Dependency Injection (DI) - Trái tim của FastAPI

Nhiều framework khác (như Flask thuần) bắt bạn phải tự quản lý việc kết nối DB, lấy user hiện tại... rất thủ công. FastAPI tích hợp sẵn hệ thống **Dependency Injection** cực mạnh.

**DI giúp giải quyết vấn đề gì?**
*   **Tái sử dụng code**: Logic lấy user từ token chỉ cần viết 1 nơi, dùng mọi chỗ.
*   **Dễ Test**: Có thể thay thế DB thật bằng DB giả khi chạy test.
*   **Gọn gàng**: Router chỉ tập trung xử lý logic, không lo việc "lấy dữ liệu ở đâu".

---

## 3.1. Cơ bản về `Depends`

Hãy tưởng tượng bạn có 3 endpoints đều cần tính toán phân trang (pagination).

**Cách làm thủ công (Dở tệ):**
```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    # Logic validate skip, limit lặp lại ở mọi nơi
    return db.query(skip, limit)

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10):
    return db.query(skip, limit)
```

**Cách dùng Dependency (Xịn):**
Định nghĩa một hàm (hoặc class) làm logic chung.
```python
from fastapi import Depends, FastAPI

app = FastAPI()

# 1. Định nghĩa Dependency
# Hàm này nhận param query và trả về dict
async def common_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# 2. Sử dụng Dependency trong Router
# commons sẽ nhận giá trị trả về từ hàm common_pagination
@app.get("/items/")
async def read_items(commons: dict = Depends(common_pagination)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(common_pagination)):
    return f"Users query: {commons}"
```
*FastAPI sẽ tự động gọi hàm `common_pagination`, lấy kết quả, và tiêm (inject) vào biến `commons`.*

---

## 3.2. Sub-dependencies (Dependency lồng nhau)

Bạn có thể xây dựng dependencies phức tạp như lego. Dependency A dùng Dependency B.

Ví dụ: 
1. `get_token_header`: Lấy token.
2. `get_current_user`: Dùng `get_token_header` để tìm user.
3. `get_active_user`: Dùng `get_current_user` để check xem user có bị block không.

```python
def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor), # Dùng lại logic trên
    last_query: str | None = Cookie(default=None)
):
    if not q:
        return last_query
    return q

@app.get("/items/")
def read_query(query_str: str = Depends(query_or_cookie_extractor)):
    return {"query": query_str}
```

---

## 3.3. Dependency cho Database (Async)

Đây là use-case phổ biến nhất: Mở kết nối DB, dùng xong, và đảm bảo ĐÓNG lại.
Chúng ta dùng `yield` thay vì `return`.

```python
# database.py giả định
SessionLocal = ... # Code tạo session SQL

# Dependency
async def get_db():
    db = SessionLocal() # 1. Mở kết nối
    try:
        yield db # 2. Trả về cho Router sử dụng
    finally:
        db.close() # 3. Đóng kết nối khi Router chạy xong (Kể cả có lỗi)

# Router
@app.post("/users/")
def create_user(user: UserCreate, db = Depends(get_db)):
    # db ở đây đã sẵn sàng sử dụng
    db.add(user)
    return user
```
*Cơ chế này tương tự `Context Manager` (with statement) nhưng dành cho API.*

---

## 3.4. Class-based Dependencies

Thay vì viết hàm, bạn có thể viết Class nếu logic phức tạp.

```python
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    # FastAPI thông minh đến mức: Depends() không điền gì cũng tự hiểu là Class cùng tên
    # Hoặc viết tắt: commons: CommonQueryParams = Depends() 
    return commons
```

---

## 3.5. Global Dependencies

Bạn muốn **TẤT CẢ** các request đều phải kiểm tra Header `X-Token`? Không cần gõ lại ở từng router.

```python
async def verify_token(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# Áp dụng cho toàn bộ app
app = FastAPI(dependencies=[Depends(verify_token)])

@app.get("/items/") # Tự động bị check token
def read_items():
    pass

@app.get("/users/") # Cũng bị check token luôn
def read_users():
    pass
```

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **Refactor Pagination**:
    *   Thử viết router `/todos` lấy danh sách công việc.
    *   Tự viết hàm Dependency `pagination_params` nhận vào `page` và `page_size` (thay vì skip/limit). Tính toán offset và trả về tuple `(limit, offset)`.
2.  **Fake Authen**:
    *   Viết Dependency `get_current_user` giả: Đọc header `Authorization`. Nếu header = "admin", trả về user dict `{"username": "admin"}`. Nếu không, trả về lỗi 401 Unauthorized.
    *   Áp dụng nó vào router `POST /todos` (Chỉ admin mới được tạo todo).
3.  **Logging**:
    *   Viết một dependency `log_request_id` đơn giản: In ra console "Request started", `yield`, sau đó in ra "Request finished".
    *   Gắn nó vào API để xem log chạy như thế nào (trước và sau khi request xử lý).

*Hiểu được Dependency Injection là bạn đã nắm được "linh hồn" của FastAPI. Nó làm code của bạn Clean và testable đến mức đáng kinh ngạc.*
