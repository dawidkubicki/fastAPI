from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
   {"title": "Title One", "author": "Author One", "category": "Category 1"},
   {"title": "Title Two", "author": "Author Two", "category": "Category 2"},
   {"title": "Title Three", "author": "Author Three", "category": "math"},
   {"title": "Title Three", "author": "Author One", "category": "math"},
]

@app.get("/books/all_books")
async def read_all_books():
    return BOOKS

@app.get("/books/mybook")
async def read_favourite_book():
    return {
        'My favourite book'
    }

@app.get("/books/byauthor/")
async def read_all_books_from_author(book_author: str):
    filtered_books=[]
    for i in range(len(BOOKS)):
        if BOOKS[i].get('author').casefold() == book_author.casefold():
            filtered_books.append(BOOKS[i])
    return filtered_books

@app.get("/books/{book_title}")
async def read_book(book_title):
    for book in BOOKS:
        if book.get('title').casefold() == str(book_title).casefold():
            return book
        
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

@app.delete("books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold == book_title.casefold():
            BOOKS.pop(i)
            break
