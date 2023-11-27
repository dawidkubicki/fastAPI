from fastapi import FastAPI

app = FastAPI()

BOOKS = [
   {"title": "Title One", "author": "Author One", "category": "Category 1"},
   {"title": "Title Two", "author": "Author Two", "category": "Category 2"},
   {"title": "Title Three", "author": "Author Three", "category": "Category 3"},
]

@app.get("/books")
async def first_api():
    return BOOKS