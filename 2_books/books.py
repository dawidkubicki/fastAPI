from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating 

class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)


BOOKS = [
    Book(1, "Echoes of Tomorrow", "Isabella Knight", "A captivating sci-fi tale set in a future where humanity grapples with the ethics of time travel.", 4),
    Book(2, "Shadows in the Mist", "Aaron Lee", "A suspenseful thriller that takes readers on a journey through a foggy town with a hidden secret.", 4),
    Book(3, "The Last Symphony", "Isabella Knight", "An emotional story of a composer's final masterpiece in war-torn Europe.", 3),
    Book(4, "Beneath the Starlit Sea", "David Harper", "An underwater adventure uncovering the mysteries of a sunken city.", 3),
    Book(5, "Whispers of the Past", "Rachel Green", "A historical novel that intertwines multiple generations in a centuries-old mansion.", 5),
    Book(6, "Flight of the Sparrow", "Mohammed Al-Fayed", "A poignant tale of freedom and resilience through the eyes of a captured bird.", 5),
    Book(7, "Chronicles of the Forgotten", "Liu Yang", "Epic fantasy about a lost civilization and the quest to unveil its history.", 5),
    Book(8, "The Glass Painter", "Isabella Knight", "Romantic story set in Paris about an artist who paints stories on glass.", 4),
    Book(9, "The Quantum Paradox", "Neil Robertson", "A mind-bending science fiction exploring the possibilities of quantum realities.", 5),
    Book(10, "Silent Echoes", "Amelia Johnson", "A gripping mystery about an investigator with the ability to hear the past.", 4),
    Book(11, "The Garden of Time", "Carlos Rodriguez", "A magical realism story about a garden where time moves differently.", 4),
    Book(12, "Into the Abyss", "Hannah Lee", "An adventure novel about a treacherous journey into an unexplored abyss.", 5),
    Book(13, "The Last Manuscript", "Alexander Ivanov", "A historical fiction about the discovery of a revolutionary ancient manuscript.", 2),
    Book(14, "Dreams of the Silent City", "Fatima Al Mansouri", "An enchanting tale set in a city where everyone communicates without words.", 2),
    Book(15, "The Alchemist's Heir", "John Smith", "A young adult fantasy about the descendant of an alchemist uncovering family secrets.", 1),
]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(add_book_id(new_book))

def add_book_id(book: Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id+1
    else:
        book.id = 1
    return book