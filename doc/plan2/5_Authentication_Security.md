# 5. Authentication & Security (Bảo mật Ứng dụng)

Một API không có bảo mật giống như nhà mở toang cửa. Bất kỳ ai cũng có thể vào xóa dữ liệu.
Chúng ta sẽ triển khai chuẩn **OAuth2 với Password Flow và JWT (JSON Web Tokens)** - Chuẩn mực của web hiện đại.

---

## 5.1. Cài đặt thư viện Bảo mật

```bash
# python-jose: Xử lý tạo/đọc JWT
# passlib[bcrypt]: Mã hóa mật khẩu (Hashing)
# python-multipart: Để xử lý Form login (OAuth2 yêu cầu gửi form, không phải JSON)
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

---

## 5.2. Password Hashing (Mã hóa mật khẩu)

**Nguyên tắc vàng**: KHÔNG BAO GIỜ lưu mật khẩu gốc (plain-text) vào Database. Phải Hash nó.

```python
from passlib.context import CryptContext

# Khởi tạo context dùng thuật toán bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Mã hóa pass: '123456' -> '$2b$12$...' """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """So khớp pass user nhập với pass trong DB"""
    return pwd_context.verify(plain_password, hashed_password)
```

---

## 5.3. JWT (JSON Web Tokens) là gì?

Thay vì lưu session trên server (tốn RAM), server cấp cho Client 1 cái "thẻ bài" (Token).
Mỗi lần Client muốn lấy dữ liệu, phải chìa thẻ bài này ra.
Server chỉ cần kiểm tra chữ ký trên thẻ (Signature) để biết thẻ thật hay giả.

Cấu trúc JWT: `Header.Payload.Signature`

---

## 5.4. Quy trình Đăng nhập (Login Flow)

### Bước 1: API Login (Cấp Token)

```python
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

# Secret Key (Giữ bí mật tuyệt đối, thường để trong biến môi trường .env)
SECRET_KEY = "supper_secret_key_123"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30) # Token sống 30p
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Tìm user trong DB theo form_data.username
    # user = get_user(db, form_data.username) ...
    
    # 2. Verify password
    # if not verify_password(form_data.password, user.hashed_password):
    #     raise HTTPException...
    
    # 3. Tạo Token
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

---

## 5.5. Quy trình Bảo vệ Endpoint (Protect Route)

### Bước 2: Dependency `get_current_user`

Hàm này sẽ chặn cửa mọi request có token không hợp lệ.

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Chỉ định nơi lấy token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Giải mã token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    # (Optional) Lấy user từ DB để chắc chắn user chưa bị xóa/block
    # user = get_user_by_username(username)
    return username # Hoặc trả về object User đầy đủ
```

### Bước 3: Sử dụng

```python
@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user, "message": "Bạn đã đăng nhập thành công!"}
```
*   Nếu gọi `/users/me` mà không có Header `Authorization: Bearer <token>` -> **Lỗi 401 Not Authenticated**.
*   Nếu có Token xịn -> Trả về dữ liệu.

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **Chức năng Register (Đăng ký)**:
    *   Tạo API `POST /register` nhận username/password.
    *   Hash password rồi lưu vào DB (sử dụng kiến thức bài Database).
2.  **Chức năng Login**:
    *   Implement hoàn chỉnh logic `login_for_access_token` kết nối với DB thật.
    *   Dùng Postman gửi `x-www-form-urlencoded` (username, password) đến `/token`.
    *   Nhận về chuỗi JWT.
3.  **Secure Todo API**:
    *   Sửa bảng `Todo`, thêm cột `owner_id`.
    *   Sửa API `Create Todo`: Lấy `current_user` từ token, gán `owner_id = current_user.id`.
    *   Sửa API `Get Todos`: Chỉ trả về các todo của chính user đó (User A không thấy todo của User B).

*Làm được bài tập 3 là bạn đã chính thức tốt nghiệp khóa "Backend cơ bản". Bạn đã có một ứng dụng Multi-user hoàn chỉnh!*
