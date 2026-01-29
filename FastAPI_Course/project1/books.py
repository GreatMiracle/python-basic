from fastapi import FastAPI

app = FastAPI()

# ======================
# FAKE DATABASE
# ======================
BOOKS = [
    {
        "id": 1,
        "title": "Title One",
        "author": "Author One",
        "category": "Science",
        "rating": 5
    },
    {
        "id": 2,
        "title": "Title Two",
        "author": "Author Two",
        "category": "History",
        "rating": 4
    },
    {
        "id": 3,
        "title": "Title Three",
        "author": "Author Three",
        "category": "Math",
        "rating": 3
    }
]

# ======================
# GET ALL BOOKS
# ======================
@app.get("/books")
async def read_all_books():
    return BOOKS


# ======================
# GET BOOK BY ID
# ======================
@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return {"message": "Book not found"}


# ======================
# GET BOOK BY RATING
# ======================
@app.get("/books/by-rating/{rating}")
async def read_book_by_rating(rating: int):
    books = []
    for book in BOOKS:
        if book["rating"] == rating:
            books.append(book)
    return books


# ======================
# CREATE BOOK
# ======================
@app.post("/books/create_book")
async def create_book(book: dict):
    BOOKS.append(book)
    return {"message": "Book created successfully"}


# ======================
# UPDATE BOOK
# ======================
@app.put("/books/update_book")
async def update_book(book: dict):
    for i in range(len(BOOKS)):
        if BOOKS[i]["id"] == book["id"]:
            BOOKS[i] = book
            return {"message": "Book updated successfully"}
    return {"message": "Book not found"}


# ======================
# DELETE BOOK
# ======================
@app.delete("/books/delete_book/{book_id}")
async def delete_book(book_id: int):
    for book in BOOKS:
        if book["id"] == book_id:
            BOOKS.remove(book)
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}
