import uvicorn
from fastapi import FastAPI, HTTPException, status, Body, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# ======================
# BOOK CLASS (MODEL)
# ======================
class Book:
    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


# ======================
# Pydantic REQUEST MODEL (VALIDATION)
# ======================
# class BookRequest(BaseModel):
#     title: str
#     author: str
#     description: str
#     rating: int

# Pydantic model – dùng để validate request từ client
class BookRequest(BaseModel):
    id: Optional[int] = Field(None, description="ID is not needed on create")
    title: str = Field(..., min_length=3, description="Tiêu đề sách")
    author: str = Field(..., min_length=1, description="Tên tác giả")
    description: str = Field(..., min_length=1, max_length=100, description="Mô tả sách")
    rating: int = Field(..., gt=0, le=5, description="Điểm đánh giá từ 1 đến 5")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "A new book",
                    "author": "Coding with Ruby",
                    "description": "A new description of a book",
                    "rating": 5
                }
            ]
        }
    }
# ======================
# FAKE DATABASE
# ======================
BOOKS: List[Book] = [
    Book(1, "Computer Science Pro", "Coding with Ruby", "A very nice book!", 5),
    Book(2, "Be Fast with FastAPI", "Coding with Ruby", "A great book!", 5),
    Book(3, "Master Endpoints", "Coding with Ruby", "An awesome book!", 5),
    Book(4, "HP1", "Author 1", "Book description", 2),
    Book(5, "HP2", "Author 2", "Book description", 3),
    Book(6, "HP3", "Author 3", "Book description", 1)
]


# ======================
# HELPER FUNCTION
# ======================
def book_to_dict(book: Book):
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "description": book.description,
        "rating": book.rating,
    }

def list_book_to_dict(books_list):
    return [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
            "rating": book.rating
        }
        for book in books_list
    ]

# Hàm phụ trợ: tự động sinh ID
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


# ======================
# GET ALL BOOKS
# ======================
# @app.get("/books", status_code=status.HTTP_200_OK)
# async def read_all_books():
#     return [book_to_dict(book) for book in BOOKS]
@app.get("/books")
async def read_all_books():
    return BOOKS

# ======================
# GET BOOK BY ID
# ======================
# @app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
# async def read_book(book_id: int):
#     for book in BOOKS:
#         if book.id == book_id:
#             return book_to_dict(book)
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Book not found"
#     )

@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(..., gt=0, description="ID sách phải lớn hơn 0")):
    """
    Lấy thông tin một cuốn sách theo ID.
    """
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Item not found"
    )

    # Nếu không tìm thấy → FastAPI tự trả về 404 Not Found (sẽ cải thiện sau)

# ======================
# CREATE BOOK
# ======================
# @app.post("/books", status_code=status.HTTP_201_CREATED)
# async def create_book(book: BookRequest):
#     new_book = Book(
#         id=len(BOOKS) + 1,
#         title=book.title,
#         author=book.author,
#         description=book.description,
#         rating=book.rating
#     )
#     BOOKS.append(new_book)
#     return book_to_dict(new_book)

# POST - Tạo sách mới
@app.post("/create-book")
async def create_book(book_request: BookRequest):

    """
    Tạo sách mới:
    - Validate dữ liệu đầu vào bằng Pydantic
    - Tự động sinh ID tăng dần
    - Thêm vào danh sách và trả về sách mới
    """
    # new_book = Book(**book_request.model_dump())
    # BOOKS.append(new_book)
    # return book_to_dict(new_book)
    # return list_book_to_dict(BOOKS)

    # Chuyển Pydantic model thành Book object
    new_book = Book(**book_request.model_dump(exclude_unset=True))  # exclude_unset=True để bỏ qua id=None
    find_book_id(new_book)  # Gán ID tự động
    BOOKS.append(new_book)

    return new_book  # Trả về sách vừa tạo (chuẩn REST)

# ======================
# UPDATE BOOK
# ======================
@app.put("/books/{book_id}", status_code=status.HTTP_200_OK)
async def update_book(book_request: BookRequest):
    for book in BOOKS:
        if book.id == book_request.id:
            book.title = book_request.title
            book.author = book_request.author
            book.description = book_request.description
            book.rating = book_request.rating
            return book_to_dict(book)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


# ======================
# DELETE BOOK
# ======================
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(..., gt=0, description="ID sách phải lớn hơn 0")):
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            return {"message": f"Book with id {book_id} deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )

# GET - Lọc sách theo rating (query parameter - mới thêm)
@app.get("/books/rating/{book_rating}")
async def read_books_by_rating(book_rating: int ):
    """
    Lọc và trả về danh sách sách có rating bằng giá trị được truyền.
    Ví dụ: /books/rating/?book_rating=5
    """
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/rating-other/")
async def read_books_by_rating_other(book_rating: int = Query(1, ge=1, le=5)):
    """
    Lọc và trả về danh sách sách có rating bằng giá trị được truyền.
    Ví dụ: /books/rating/?book_rating=5
    """
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

if __name__ == "__main__":
    uvicorn.run("books:app", host="127.0.0.1", port=8000, reload=True)