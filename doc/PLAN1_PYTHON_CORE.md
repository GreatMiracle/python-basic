# KẾ HOẠCH CHI TIẾT: PYTHON CORE MASTERY

File này chi tiết hóa phần **"1. Python Core"** từ [MASTER_PLAN.md](./MASTER_PLAN.md). Đây là danh sách các đầu mục kiến thức cụ thể bạn cần học để nắm vững ngôn ngữ Python, tạo nền tảng vững chắc trước khi bước vào FastAPI.

---

## 1. Môi trường & Quản lý Gói (Environment & Package Management)
*Học cách thiết lập môi trường làm việc chuyên nghiệp, tránh xung đột thư viện.*

*   [ ] **Virtual Environments**:
    *   Hiểu lý do tại sao cần môi trường ảo.
    *   `venv`: Tạo, kích hoạt, vô hiệu hóa (Standard library).
    *   `poetry`: Công cụ quản lý dependency hiện đại (Khuyên dùng cho production).
*   [ ] **PIP**:
    *   Lệnh cơ bản: `install`, `uninstall`, `freeze`, `list`.
    *   File quản lý: `requirements.txt`.
*   [ ] **Module & Import System**:
    *   Cách Python tìm kiếm module (`sys.path`).
    *   Absolute Imports vs Relative Imports (dấu `.` và `..`).
    *   Vai trò của file `__init__.py` (biến folder thành package).
    *   `if __name__ == "__main__":`: Entry point của script.

## 2. Cấu trúc dữ liệu & Giải thuật cơ bản (Data Structures)
*Hiểu sâu về công cụ lưu trữ dữ liệu để chọn loại phù hợp tối ưu hiệu năng.*

*   [ ] **Primitive Types**: `int`, `float`, `bool`, `str`, `NoneType`.
*   [ ] **String Manipulation**:
    *   F-strings (Format string hiện đại).
    *   Slicing `[start:step:end]`, Splitting, Joining via `join()`.
    *   Encoding/Decoding (`utf-8` vs `bytes`).
*   [ ] **List (Mảng động)**:
    *   Memory allocation & Dynamic resizing (cơ chế bên trong).
    *   Operations: `append` vs `extend`, `sort` vs `sorted`.
    *   List Comprehension (viết code gọn).
*   [ ] **Dictionary (Hash Map - Cực quan trọng)**:
    *   Cơ chế Hashing (tại sao key phải immutable?).
    *   Dict Comprehension.
    *   Methods: `.get()`, `.setdefault()`, `.items()`, `.keys()`.
    *   Merging dicts (Python 3.9+ `|` operator).
*   [ ] **Set & Tuple**:
    *   `Set`: Lý thuyết tập hợp (union, intersection), khử trùng lặp.
    *   `Tuple`: Immutability, Unpacking (`x, y = y, x`).
*   [ ] **Advanced Collections (`collections` module)**:
    *   `Counter`: Đếm phần tử nhanh.
    *   `defaultdict`: Xử lý missing keys thông minh.
    *   `namedtuple`: Tuple có tên (tiền thân của Dataclass).

## 3. Hàm & Lập trình hàm (Functions & Functional Programming)
*Viết logic tái sử dụng, gọn gàng và xử lý dữ liệu mạnh mẽ.*

*   [ ] **Function Basics**:
    *   Parameters: Positional, Keyword arguments.
    *   `*args` và `**kwargs`: Tham số động.
    *   Default mutable arguments trap (Lỗi sơ đẳng khi dùng list làm default param).
*   [ ] **Scope & Namespaces**:
    *   Quy tắc LEGB (Local, Enclosing, Global, Built-in).
    *   Keyword `global` và `nonlocal`.
*   [ ] **Functional Tools**:
    *   `lambda`: Hàm vô danh.
    *   `map()`, `filter()`: Xử lý sequence.
    *   `zip()`: Ghép cặp dữ liệu, `enumerate()`: Duyệt kèm index.
*   [ ] **Decorators (Cốt lõi của FastAPI)**:
    *   Higher-order functions (Hàm trả về hàm).
    *   Viết Decorator cơ bản.
    *   `functools.wraps`: Giữ metadata cho hàm được wrap.
    *   Decorators có tham số.
*   [ ] **Generators & Iterators**:
    *   `iter()` và `next()`.
    *   Keyword `yield` và `yield from`.
    *   Generator Expressions (tiết kiệm bộ nhớ hơn List Comprehension).

## 4. Lập trình hướng đối tượng (Advanced OOP)
*Tổ chức code cho các dự án lớn, hiểu cách các thư viện được xây dựng.*

*   [ ] **Class & Instance**:
    *   `self`: Ý nghĩa thực sự.
    *   Class variables vs Instance variables.
*   [ ] **Methods**:
    *   Instance Method.
    *   `@classmethod`: Phương thức của lớp (thường dùng làm Factory constructor).
    *   `@staticmethod`: Hàm tiện ích gắn vào class.
*   [ ] **Magic Methods (Dunder Methods)**:
    *   Lifecycle: `__init__`, `__new__` (ít dùng nhưng đáng biết), `__del__`.
    *   Representation: `__str__` (cho user), `__repr__` (cho dev).
    *   Container emulation: `__getitem__`, `__setitem__`, `__len__`, `__contains__`.
    *   Comparison: `__eq__`, `__lt__`,...
*   [ ] **Kế thừa & Đa hình**:
    *   Inheritance cơ bản.
    *   `super()`: Gọi phương thức cha đúng cách.
    *   Multiple Inheritance & MRO (Method Resolution Order).
*   [ ] **Encapsulation & Abstraction**:
    *   Property decorators: `@property`, `@x.setter`.
    *   Access Modifiers qui ước (`_protected`, `__private`).
    *   Abstract Base Classes (`abc` module): Bắt buộc class con phải implement methods.
*   [ ] **Dataclasses (`dataclasses` module)**:
    *   Tạo class lưu dữ liệu nhanh chóng (giống Pydantic nhưng built-in).

## 5. Modern Python & Type Hinting (Nền tảng của FastAPI)
*Python hiện đại không còn là ngôn ngữ "động" hoàn toàn, Type Hint giúp code an toàn và dễ maintain.*

*   [ ] **Basic Typing**:
    *   `int`, `str`, `float`, `bool`.
    *   `List[int]`, `Dict[str, int]`, `Set[str]` (hoặc dùng generic built-in từ Python 3.9+).
*   [ ] **Special Types (`typing` module)**:
    *   `Optional[T]`: Có thể là T hoặc None.
    *   `Union[A, B]`: Có thể là kiểu A hoặc kiểu B.
    *   `Any`: Tắt check type (hạn chế dùng).
    *   `Callable`: Kiểu dữ liệu hàm.
    *   `TypeVar` & Generics: Viết hàm xử lý nhiều kiểu dữ liệu chung.
*   [ ] **Static Analysis**: Kiểm tra code bằng `mypy`.

## 6. Xử lý Lỗi & I/O (Error Handling & I/O)
*Kiểm soát luồng chạy khi có sự cố và tương tác với thế giới bên ngoài.*

*   [ ] **Exception Handling**:
    *   `try` / `except` / `else` / `finally`.
    *   Bắt cụ thể từng loại lỗi, tránh bắt `Exception` chung chung.
    *   `raise`: Tự ném lỗi.
    *   Custom Exceptions: Tạo class lỗi nghiệp vụ riêng.
*   [ ] **File Handling**:
    *   Context Manager (`with open(...)`): Đảm bảo file luôn đóng.
    *   Modes: `r`, `w`, `a`, `b`.
    *   JSON serialization: `json.load()`, `json.dump()`.
*   [ ] **Path Handling (`pathlib`)**:
    *   Tư duy hướng đối tượng với đường dẫn (thay thế `os.path`).
    *   Construct paths, check exists, read/write text trực tiếp.

## 7. Python Internals & Advanced Topics (Nâng cao)
*Hiểu sâu để tối ưu hiệu năng và xử lý các vấn đề hóc búa.*

*   [ ] **Memory Management**:
    *   Reference Counting.
    *   Garbage Collection.
    *   Deep copy vs Shallow copy (`copy` module).
*   [ ] **Concurrency Models** (Intro - chuẩn bị cho Backend):
    *   Phân biệt Process vs Thread.
    *   GIL (Global Interpreter Lock): Tại sao Multithreading Python không tận dụng hết CPU core?
    *   Sync vs Async concept.
*   [ ] **Context Managers**:
    *   Tự viết Context Manager dùng class (`__enter__`, `__exit__`).
    *   Dùng `contextlib.contextmanager` decorator.

---
**Hướng dẫn sử dụng file này**:
1.  Đi từ trên xuống dưới, không được nhảy cóc các phần Bắt buộc.
2.  Với mỗi đầu mục, hãy Google keywords, đọc document và viết 1 file code ví dụ nhỏ (snippet) để hiểu cách nó chạy.
3.  Khi học đến phần 5 (Type Hinting), hãy bắt đầu áp dụng nó ngược lại cho các code bài tập trước đó.
