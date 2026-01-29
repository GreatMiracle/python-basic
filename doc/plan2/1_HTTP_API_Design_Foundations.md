# 1. Nền tảng HTTP & Thiết kế API (HTTP & API Design Foundations)

Trước khi viết bất kỳ dòng code FastAPI nào, bạn cần hiểu "ngôn ngữ" mà Web sử dụng để giao tiếp: **HTTP**.
Làm Backend mà không hiểu HTTP giống như làm bác sĩ mà không hiểu giải phẫu cơ thể người vậy.

---

## 1.1. Giải phẫu một HTTP Request & Response

Mọi giao tiếp trên web đều tuân theo mô hình **Khách (Client) hỏi - Chủ (Server) trả lời**.

### Cấu trúc một Request (Client gửi đi)
Gồm 3 phần chính:
1.  **Start Line**: Chứa Method (Hành động) + URL (Địa chỉ) + Version.
2.  **Headers**: Meta-data (Thông tin phụ: gửi định dạng gì, ai gửi...).
3.  **Body** (Tùy chọn): Dữ liệu gửi kèm (thường dùng khi tạo/sửa).

*Ví dụ bản tin HTTP thô (Raw HTTP):*
```http
POST /users/register HTTP/1.1
Host: api.example.com
Content-Type: application/json
User-Agent: PostmanRuntime/7.26

{
    "username": "anti_dev",
    "password": "secret_password"
}
```

### Cấu trúc một Response (Server trả về)
1.  **Status Line**: Version + Status Code (Mã kết quả) + Reason Phrase.
2.  **Headers**: Meta-data (Server là gì, trả về định dạng gì...).
3.  **Body**: Dữ liệu kết quả (thường là JSON).

*Ví dụ phản hồi:*
```http
HTTP/1.1 201 Created
Date: Mon, 27 Jul 2023 12:28:53 GMT
Content-Type: application/json

{
    "id": 101,
    "message": "User created successfully"
}
```

---

## 1.2. HTTP Methods - Những động từ của Web

Bạn không thể dùng bừa bãi các method. Hãy dùng đúng semantic (ngữ nghĩa) của nó.

| Method | Ý nghĩa | Có Body không? | Ví dụ |
| :--- | :--- | :--- | :--- |
| **GET** | **Lấy dữ liệu**. Không được thay đổi gì trên server. | Không | `GET /products` (Xem ds sản phẩm) |
| **POST** | **Tạo mới** một tài nguyên. | Có | `POST /orders` (Đặt hàng mới) |
| **PUT** | **Cập nhật toàn bộ** (Thay thế hoàn toàn). | Có | `PUT /users/1` (Gửi full thông tin để đè lên user cũ) |
| **PATCH** | **Cập nhật một phần** (Sửa vài trường). | Có | `PATCH /users/1` (Chỉ gửi field `email` để sửa email) |
| **DELETE**| **Xóa** tài nguyên. | Không | `DELETE /comments/5` (Xóa comment số 5) |

**Sai lầm phổ biến**: Dùng `GET` để xóa dữ liệu (Ví dụ: `GET /delete-user?id=1`).
-> **Nguy hiểm!** Các trình duyệt hoặc crawler có thể tự động gọi link này và xóa sạch dữ liệu của bạn. Hãy luôn dùng `DELETE`.

---

## 1.3. HTTP Status Codes - Ngôn ngữ của Server

Đừng chỉ trả về `200 OK` cho mọi thứ. Frontend Dev sẽ "ghét" bạn nếu bạn làm thế.

*   **2xx: Success (Thành công)**
    *   `200 OK`: Thành công chung (GET, PUT, PATCH).
    *   `201 Created`: Tạo mới thành công (thường dùng cho POST).
    *   `204 No Content`: Thành công nhưng không có dữ liệu trả về (thường dùng cho DELETE).

*   **4xx: User Error (Lỗi do người gửi)**
    *   `400 Bad Request`: Gửi sai format, thiếu trường bắt buộc.
    *   `401 Unauthorized`: Chưa đăng nhập.
    *   `403 Forbidden`: Đã đăng nhập nhưng không có quyền (User thường đòi vào trang Admin).
    *   `404 Not Found`: Không tìm thấy tài nguyên.
    *   `422 Unprocessable Entity`: Dữ liệu đúng format nhưng sai logic (ví dụ email không hợp lệ) - *FastAPI dùng cái này rất nhiều*.

*   **5xx: Server Error (Lỗi do bạn code dở)**
    *   `500 Internal Server Error`: Code bị crash, exception không được xử lý.

---

## 1.4. Thiết kế RESTful API chuẩn mực

REST (Representational State Transfer) là một bộ quy tắc thiết kế.

### Quy tắc 1: URL là Danh từ, không phải Động từ
Tài nguyên (Resource) là danh từ. Hành động (Action) nằm ở HTTP Method.

*   ❌ **Sai (Kiểu RPC cũ):**
    *   `/getAllUsers`
    *   `/createNewUser`
    *   `/updateUser/1`
    *   `/deleteUser/1`

*   ✅ **Đúng (RESTful):**
    *   `GET /users` (Lấy danh sách)
    *   `POST /users` (Tạo mới)
    *   `PUT /users/1` (Sửa user 1)
    *   `DELETE /users/1` (Xóa user 1)

**Tại sao?** Vì nó thống nhất và dễ đoán. Nhìn vào `/users` là biết ngay đang thao tác với User, method sẽ cho biết làm gì.

### Quy tắc 2: Phân cấp cha - con
Nếu muốn lấy "Các comment của bài viết số 5":
*   `GET /posts/5/comments`

Nếu muốn lấy "Comment số 10" (không quan tâm bài viết nào):
*   `GET /comments/10`

### Quy tắc 3: Versioning (Đánh phiên bản)
Luôn luôn (Always) để version trong URL để sau này nâng cấp không làm hỏng app cũ.
*   `/v1/products`
*   `/v2/products`

---

## 1.5. Tools cần thiết

1.  **Postman**: Công cụ số 1 để test API thủ công. Bạn có thể lưu các request lại, chia sẻ cho team.
2.  **Swagger UI / Open API**: Khi code FastAPI, truy cập `/docs`, bạn sẽ thấy giao diện này tự động được tạo ra. Nó cho phép test API ngay trên trình duyệt mà không cần cài Postman.
3.  **Curl**: Lệnh dòng lệnh (dành cho dân Linux/Server).
    ```bash
    # Ví dụ gọi API bằng curl
    curl -X GET "https://api.example.com/v1/users" -H "accept: application/json"
    ```

---

## BÀI TẬP (Action Items)

1.  **Phân tích API thực tế**:
    *   Vào trang [JSONPlaceholder](https://jsonplaceholder.typicode.com/).
    *   Dùng Postman (hoặc trình duyệt) gọi thử: `GET /posts`, `GET /posts/1`, `POST /posts`.
    *   Quan sát Status Code và cấu trúc JSON trả về.
2.  **Thiết kế URL trên giấy**:
    *   Giả sử bạn làm ứng dụng E-commerce. Hãy viết ra các URL và Method cho các chức năng:
        *   Xem danh sách sản phẩm.
        *   Xem chi tiết sản phẩm ID=100.
        *   User thêm sản phẩm vào giỏ hàng.
        *   User xóa sản phẩm khỏi giỏ hàng.
3.  **Thử nghiệm Status Code**:
    *   Thử truy cập một trang web không tồn tại (ví dụ `google.com/linh-tinh`) -> Xem nó báo lỗi gì (404?).
    *   Thử dùng Postman gửi request thiếu dữ liệu lên 1 API test -> Xem nó báo 400 hay 422?

*Nắm chắc lý thuyết này, bài sau chúng ta sẽ bắt đầu dòng code FastAPI đầu tiên!*
