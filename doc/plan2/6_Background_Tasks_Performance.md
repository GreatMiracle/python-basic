# 6. Background Tasks & Performance (Hiệu năng Ứng dụng)

Một API tốt phải phản hồi nhanh (dưới 200ms). Nhưng nếu phải gửi email, xử lý ảnh, hay tính toán AI report mất 10 giây thì sao?
Giải pháp: Trả về kết quả ngay lập tức cho user ("OK, đã nhận"), và xử lý việc nặng ở **Background** (Chạy ngầm).

---

## 6.1. FastAPI Background Tasks (Đơn giản - Built-in)

FastAPI hỗ trợ tính năng này ngay trong core, không cần cài thêm gì phức tạp. Dùng cho các task nhẹ nhàng (Gửi email, ghi log).

```python
from fastapi import BackgroundTasks, FastAPI
import time

app = FastAPI()

# Hàm xử lý nặng (Chạy ngầm)
def write_notification(email: str, message: str):
    time.sleep(5)  # Giả lập gửi email mất 5s
    # Ghi vào file log thay vì gửi thật
    with open("log.txt", "a") as f:
        f.write(f"Email sent to {email}: {message}\n")

@app.post("/send-notification/{email}")
async def send_notification(
    email: str, 
    background_tasks: BackgroundTasks # Dependency đặc biệt
):
    # Đăng ký task chạy ngầm
    background_tasks.add_task(write_notification, email, message="Chào mừng bạn!")
    
    # Trả về ngay lập tức cho User (không cần chờ 5s)
    return {"message": "Notification sent in the background"}
```
*User nhận được response sau 10ms. Hàm `write_notification` tiếp tục chạy ở server sau đó.*

---

## 6.2. Caching với Redis (Tăng tốc Query)

Query Database luôn tốn thời gian. Redis là Database lưu trong RAM, cực nhanh.
Mô hình: User hỏi -> Check Redis -> Nếu có thì trả luôn (Hit) -> Nếu không thì hỏi DB rồi lưu vào Redis (Miss).

**Cài đặt**:
```bash
pip install redis
# Và cần chạy Redis Server (thường dùng Docker: docker run -p 6379:6379 redis)
```

**Code ví dụ:**
```python
import redis
import json

# Kết nối Redis
r = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/heavy-data/{item_id}")
def get_heavy_data(item_id: int):
    # 1. Check Cache
    cached_value = r.get(f"item:{item_id}")
    if cached_value:
        print("Cache HIT!")
        return json.loads(cached_value)
    
    # 2. Nếu không có cache -> Tính toán/Query DB (Giả lập mất 2s)
    print("Cache MISS - Calculating...")
    data = {"id": item_id, "complex_result": item_id * 9999}
    
    # 3. Lưu vào Cache (Set expire time 60s)
    r.setex(f"item:{item_id}", 60, json.dumps(data))
    
    return data
```
*Lần đầu gọi mất 2s. Lần sau gọi mất 1ms.*

---

## 6.3. Celery (Advanced - Hàng đợi tác vụ)

Khi task quá nặng (Video transcoding, Training AI) hoặc số lượng quá lớn, `BackgroundTasks` của FastAPI là không đủ (vì nó vẫn chung process web, nếu web sập thì task mất).
**Celery** là giải pháp chuyên nghiệp: Nó chạy trên process riêng biệt (Worker), dùng Redis/RabbitMQ làm hàng đợi trung gian (Broker).

**Cấu trúc:**
1.  **FastAPI (Producer)**: Chỉ nhận request -> Đẩy task vào hàng đợi Redis.
2.  **Redis (Broker)**: Chứa danh sách task.
3.  **Celery Worker (Consumer)**: Lấy task từ Redis ra xử lý.

```python
# tasks.py
from celery import Celery
import time

# Cấu hình Celery nối với Redis
celery_app = Celery("worker", broker="redis://localhost:6379/0")

@celery_app.task
def celery_heavy_task(name: str):
    time.sleep(10)
    return f"Hello object {name}"
```

```python
# main.py (FastAPI)
from tasks import celery_heavy_task

@app.post("/process/")
def process(name: str):
    # Đẩy việc sang Celery
    celery_heavy_task.delay(name)
    return {"message": "Job submitted"}
```

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **Email Log (BackgroundTasks)**:
    *   Tạo API `/signup`.
    *   Sau khi tạo user thành công, dùng `BackgroundTasks` để ghi một dòng "Welcome user X" vào file `emails.log`. Đảm bảo API phản hồi nhanh.
2.  **Simple Cache**:
    *   Viết API `/weather/{city}`.
    *   Lần đầu gọi, giả lập `sleep(3)` rồi trả về nhiệt độ ngẫu nhiên.
    *   Lưu kết quả vào `dict` toàn cục (in-memory cache) kèm thời gian lưu.
    *   Lần sau gọi, nếu chưa quá 10s thì trả về giá trị trong `dict` ngay lập tức.
    *(Đây là cách hiểu Cache mà chưa cần cài Redis)*.

*Kiến thức phần này giúp hệ thống của bạn chịu tải cao (Scalable). Đừng bắt user chờ đợi những thứ không cần thiết!*
