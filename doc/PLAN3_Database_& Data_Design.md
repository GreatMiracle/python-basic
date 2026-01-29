# KẾ HOẠCH CHI TIẾT: DATABASE & DATA DESIGN MASTERY

File này chi tiết hóa phần **"3. Database & Data Design"** từ [MASTER_PLAN.md](./MASTER_PLAN.md).
"Data is the new oil" - Dữ liệu là tài sản quý giá nhất. Là Backend Developer, bạn có thể viết code xấu (sửa được), nhưng nếu thiết kế Database sai, việc sửa chữa sẽ cực kỳ đau đớn và tốn kém (Migration Nightmare).

---

## 1. Relational Database Fundamentals (SQL Core)
*Nắm vững ngôn ngữ truy vấn SQL (Structured Query Language). PostgreSQL là chuẩn mực khuyên dùng.*

*   [ ] **Các thành phần cơ bản**:
    *   Tables, Rows (Records), Columns (Fields).
    *   Primary Key (Khóa chính): UUID vs Integer Auto-increment.
    *   Foreign Key (Khóa ngoại): Đảm bảo toàn vẹn tham chiếu (Referential Integrity).
*   [ ] **SQL Commands**:
    *   **DDL (Data Definition)**: `CREATE TABLE`, `ALTER TABLE`, `DROP`, `TRUNCATE`.
    *   **DML (Data Manipulation)**: `INSERT`, `UPDATE`, `DELETE`.
    *   **DQL (Data Query)**: `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`.
*   [ ] **Advanced Querying**:
    *   **JOINS**: Hiểu rõ sự khác biệt giữa `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`.
    *   **Aggregation**: `GROUP BY`, `HAVING`, `COUNT`, `SUM`, `AVG`.
    *   **Subqueries & CTEs**: Common Table Expressions (`WITH clause`) giúp query dễ đọc hơn.

## 2. Database Design & Modeling (Tư duy thiết kế)
*Trước khi gõ lệnh tạo bảng, phải vẽ được sơ đồ. Sai một ly đi một dặm.*

*   [ ] **ERD (Entity Relationship Diagram)**:
    *   Cách vẽ sơ đồ thực thể - quan hệ.
    *   Tools: dbdiagram.io, Draw.io.
*   [ ] **Chuẩn hóa dữ liệu (Normalization)**:
    *   Mục đích: Giảm dư thừa (Redundancy) và dị thường dữ liệu (Anomalies).
    *   Các dạng chuẩn: 1NF, 2NF, 3NF (Thường dừng ở 3NF là đủ).
    *   **Denormalization**: Khi nào nên cố tình làm "ngược" chuẩn hóa để tăng tốc độ đọc?
*   [ ] **Các loại quan hệ**:
    *   **One-to-One (1-1)**: Thông tin phụ (User Details).
    *   **One-to-Many (1-N)**: User - Posts. (Khóa ngoại nằm ở bảng 'Many').
    *   **Many-to-Many (N-N)**: Students - Courses. (Cần bảng trung gian - Bridge/Pivot Table).

## 3. Advanced SQL & Performance Tuning (Tối ưu hóa)
*Query chạy nhanh ở local (10 dòng) nhưng chết đứng ở production (10 triệu dòng). Tại sao?*

*   [ ] **Indexing (Đánh chỉ mục)**:
    *   Cấu trúc B-Tree Index.
    *   Single Index vs Composite Index (Index trên nhiều cột).
    *   Trade-off: Index giúp đọc nhanh nhưng làm chậm ghi (Insert/Update) -> Cần cân nhắc.
*   [ ] **Query Analysis**:
    *   Sử dụng lệnh `EXPLAIN ANALYZE` để xem "Query Plan".
    *   Phân biệt **Index Scan** (Tốt) vs **Sequential Scan** (Xấu - Quét toàn bộ bảng).
*   [ ] **Transactions & ACID**:
    *   **Atomicity**: Tất cả thành công hoặc tất cả thất bại (Rollback).
    *   **Isolation Levels**: Read Committed, Repeatable Read, Serializable (Hiểu về Race Conditions).
    *   **Locking**: Deadlocks là gì và cách tránh.

## 4. NoSQL Database (Redis & MongoDB)
*Không phải lúc nào SQL cũng là giải pháp tốt nhất. Biết người biết ta.*

*   [ ] **Redis (Key-Value Store)**:
    *   Lưu trữ trên RAM -> Cực nhanh.
    *   Use-cases: Caching (giảm tải DB), Session Store, Rate Limiting, Message Broker/Queue (Pub/Sub).
    *   Data types: String, List, Set, Hash.
*   [ ] **MongoDB (Document Store)**:
    *   Schema-less: Dữ liệu JSON linh hoạt, không cấu trúc cố định.
    *   Khi nào dùng? (Log dữ liệu, Catalog sản phẩm đa dạng thuộc tính, Big Data).
    *   CAP Theorem: Consistency vs Availability.

## 5. Scaling Strategies (Kiến thức hệ thống lớn)
*Khi ứng dụng có hàng triệu users, 1 server DB là không đủ.*

*   [ ] **Replication (Sao chép)**:
    *   Master-Slave Architecture.
    *   Tách biệt Read/Write: Ghi vào Master, Đọc từ Slaves.
*   [ ] **Sharding (Phân mảnh)**:
    *   Chia nhỏ bảng to thành nhiều bảng nhỏ nằm trên các server khác nhau (Horizontal Scaling).
*   [ ] **Connection Pooling**:
    *   Tại sao mở/đóng kết nối lại đắt đỏ?
    *   Sử dụng **PgBouncer** hoặc tính năng Pooling của SQLAlchemy.

---
**Hướng dẫn học**:
1.  Bắt đầu với **Phần 1 & 2** thật kỹ với PostgreSQL. Hãy tự thiết kế DB cho một app E-commerce (User, Product, Order, OrderItem).
2.  Học **Phần 3** khi bạn đã có dữ liệu mẫu lớn (dùng script để fake 1 triệu dòng dữ liệu và thử query).
3.  **Redis** là bắt buộc phải biết để làm Backend hiện đại (kết hợp với FastAPI ở Module trước).
