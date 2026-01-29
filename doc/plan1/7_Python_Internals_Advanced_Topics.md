# 7. Python Internals & Advanced Topics (Kiến thức chuyên sâu)

Phần này phân loại giữa Junior và Senior. Hiểu những gì diễn ra bên dưới giúp bạn tối ưu code, tránh memory leak và giải thích được những hiện tượng "kỳ lạ" của Python.

---

## 7.1. Memory Management (Quản lý bộ nhớ)

Python tự động quản lý bộ nhớ, bạn không cần `malloc` hay `free` như C. Nhưng nó làm thế nào?

### 1. Reference Counting (Đếm tham chiếu)
Mọi object trong Python đều có một con số đếm xem có bao nhiêu biến đang trỏ vào nó.
*   Khi biến được gán (`a = object`): count + 1.
*   Khi biến bị xóa (`del a`) hoặc ra khỏi scope: count - 1.
*   Khi count = 0: Object bị xóa ngay lập tức -> Thu hồi RAM.

```python
import sys

a = []
# count = 2 (1 biến 'a', 1 do hàm getrefcount dùng tạm)
print(sys.getrefcount(a)) 

b = a
# count = 3 (thêm biến 'b')
print(sys.getrefcount(a)) 
```

### 2. Garbage Collection (GC) - Xử lý tham chiếu vòng
Vấn đề: Object A trỏ vào B, B trỏ ngược lại A. Cả 2 không còn ai dùng nữa, nhưng count của chúng luôn là 1 (do trỏ nhau). Reference Counting bó tay.
-> **Garbage Collector** của Python chạy định kỳ để quét và xử lý các vụ "tham chiếu vòng" này.

---

## 7.2. Mutable vs Immutable & Copying

### Shallow Copy vs Deep Copy
Đây là nguồn gốc của hàng tá bug đau đầu.

```python
import copy

original = [[1, 2], [3, 4]]

# 1. Assignment (Gán): Không copy gì cả, chỉ trỏ thêm tên gọi
a = original 
a[0][0] = 999
print(original[0][0]) # 999 (Bị thay đổi theo!)

# 2. Shallow Copy (Copy nông): Tạo list mới, nhưng phần tử bên trong vẫn trỏ về cũ
# Dùng list.copy() hoặc copy.copy()
original = [[1, 2], [3, 4]] # Reset
b = copy.copy(original)
b[0][0] = 888
print(original[0][0]) # 888 (Vẫn bị đổi! Vì List con [1,2] không được copy)

# 3. Deep Copy (Copy sâu): Copy đệ quy toàn bộ mọi thứ
original = [[1, 2], [3, 4]] # Reset
c = copy.deepcopy(original)
c[0][0] = 777
print(original[0][0]) # 1 (An toàn tuyệt đối!)
```
**Quy tắc**: Nếu object chứa object khác (nested list/dict), muốn sửa bản copy mà không ảnh hưởng bản gốc -> Bắt buộc dùng `deepcopy`.

---

## 7.3. Global Interpreter Lock (GIL)

Đây là "đặc sản" tai tiếng của Python (CPython Implementation).

**Cơ chế**: Tại một thời điểm, chỉ có **MỘT Thread** được thực thi mã bytecode Python. Dù máy bạn có 16 core CPU, một process Python multithreading vẫn chỉ ăn max 1 core.

**Hệ quả (Bắt buộc nhớ)**:
*   **CPU-bound tasks** (Tính toán nặng, xử lý ảnh, AI): Multithreading **VÔ DỤNG** (có khi còn chậm hơn do context switch). -> Phải dùng `Multiprocessing` (chạy nhiều process riêng biệt).
*   **I/O-bound tasks** (Gọi API, đọc file, truy vấn DB): Multithreading **RẤT TỐT**. Trong lúc chờ mạng phản hồi, GIL được nhả ra cho thread khác chạy. -> Đây là lý do Backend Python (như FastAPI) vẫn nhanh, vì Web App chủ yếu là I/O bound.

---

## 7.4. Concurrency Models: Threading vs Multiprocessing vs AsyncIO

Để làm Backend, bạn cần phân biệt rõ 3 anh này:

| Feature | Multiprocessing | Threading | AsyncIO (FastAPI dùng cái này) |
| :--- | :--- | :--- | :--- |
| **Cơ chế** | Tạo Process mới (riêng RAM) | Tạo Thread trong 1 Process (chung RAM) | Single Thread, Event Loop |
| **Sử dụng cho** | CPU-bound (Encoding video, ML) | I/O-bound (Cũ - Flask/Django cũ) | I/O-bound (Mới - High Concurrency) |
| **Ưu điểm** | Tận dụng đa nhân CPU | Đơn giản, quen thuộc | Cực nhẹ, xử lý hàng rưỡi request |
| **Nhược điểm** | Tốn RAM, giao tiếp khó | Bị GIL, khó debug Race Condition | Code phức tạp (`async/await`) |

**Ví dụ AsyncIO (Cốt lõi FastAPI)**:
```python
import asyncio

async def nau_com():
    print("Bắt đầu nấu cơm...")
    await asyncio.sleep(3) # Giả lập chờ đợi, nhường CPU cho việc khác
    print("Cơm chín!")

async def luoc_rau():
    print("Bắt đầu luộc rau...")
    await asyncio.sleep(2)
    print("Rau chín!")

async def main():
    # Chạy song song cả 2 việc cùng lúc
    await asyncio.gather(nau_com(), luoc_rau())

if __name__ == "__main__":
    asyncio.run(main()) 
```
*Kết quả: Tổng thời gian là 3s (việc lâu nhất), thay vì 5s (3+2).*

---

## BÀI TẬP THỰC HÀNH (Action Items)

1.  **Deepcopy Experiment**:
    *   Tạo một dict phức tạp: `data = {"config": {"a": 1}, "users": [1, 2]}`.
    *   Thử dùng phép gán `=`, `copy`, và `deepcopy` rồi sửa dữ liệu con để thấy sự khác biệt.
2.  **CPU Stress Test**:
    *   Viết hàm tính giai thừa số lớn.
    *   Dùng module `threading` để chạy 2 thread tính toán cùng lúc. Đo thời gian.
    *   Dùng module `multiprocessing` để chạy 2 process tính toán cùng lúc. Đo thời gian.
    *   So sánh để thấy GIL "dìm hàng" Threading thế nào trong tác vụ CPU.
3.  **Async Hello World**:
    *   Viết script AsyncIO tải nội dung 3 trang web giả lập (dùng `asyncio.sleep` thay cho request thật).
    *   In ra thời gian bắt đầu và kết thúc của từng request để chứng minh chúng chạy xen kẽ nhau (concurrently).

*Lời kết: Chúc mừng bạn đã đi hết chặng đường Python Core! Kiến thức ở phần 7 này là hành trang để bạn giải thích "Tại sao?" khi gặp các vấn đề hiệu năng trong thực tế.*
