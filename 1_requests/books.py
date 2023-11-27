from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
   {"title": "Title One", "author": "Author One", "category": "Category 1"},
   {"title": "Title Two", "author": "Author Two", "category": "Category 2"},
   {"title": "Title Three", "author": "Author Three", "category": "math"},
   {"title": "Title Three", "author": "Author One", "category": "math"},
]

@app.get("/books/mybook")
async def read_favourite_book():
    return {
        'My favourite book'
    }

@app.get("/books/{book_title}")
async def read_book(book_title):
    for book in BOOKS:
        if book.get('title').casefold() == str(book_title).casefold():
            return book
        
@app.get("/books/{book_author}/")
async def read_category_by_query(book_author: str, category: str):
   books_to_return = []
   for book in BOOKS:
      if book.get('author').casefold() == book_author.casefold() and \
         book.get('category').casefold() == category.casefold():
         books_to_return.append(book)
   
   return books_to_return

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)