from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

Books = {
    'book_1':{'title':'Book 1', 'author':'Author 1'},
    'book_2':{'title':'Book 2', 'author':'Author 2'},
    'book_3':{'title':'Book 3', 'author':'Author 3'},
    'book_4':{'title':'Book 4', 'author':'Author 4'},
    'book_5':{'title':'Book 5', 'author':'Author 5'},
}

@app.get("/")
async def first_api():
    return {"message": "Hello World"}

@app.get("/books")
async def read_all_books():
    return Books

@app.get("/skipbooks")
async def read_all_books(skip_book: str = "book_3"):
    new_books = Books.copy()
    del new_books[skip_book]
    return new_books

@app.get("/skbooks")
async def read_all_books(skip_book: Optional[str]=None):
    new_books = Books.copy()
    if skip_book:
        del new_books[skip_book]
    return new_books

@app.get("/books/{book_id}")
async def read_book(book_id :str):
    return Books[book_id]

class DirectionName(str, Enum):
    north = "north"
    south = "south"
    east = "east"
    west = "west"

@app.get("/direction/{direction_name}")
async def read_direction(direction_name : DirectionName):
    if direction_name == DirectionName.north:
        return {"direction": direction_name, "description": "go north"}
    elif direction_name == DirectionName.south:
        return {"direction": direction_name, "description": "go south"}
    elif direction_name == DirectionName.east:
        return {"direction": direction_name, "description": "go east"}
    elif direction_name == DirectionName.west:
        return {"direction": direction_name, "description": "go west"}
    else:
        return {"direction": direction_name, "description": "invalid direction"}


@app.post("/create")
async def create_book(title: str, author: str):
    book_id = str(len(Books) + 1)
    Books[f'book_{book_id}'] = {'title':title, 'author':author}
    return Books[f'book_{book_id}']


@app.put("/update/{book_id}")
async def update_book(book_id: str, title: str, author: str):
    Books[book_id] = {'title':title, 'author':author}
    return Books[book_id]


@app.delete("/delete/{book_id}")
async def delete_book(book_id: str):
    del Books[book_id]
    return Books

@app.get("/assignment/")
async def read_book_assignment(book_id: str):
    return Books[book_id]