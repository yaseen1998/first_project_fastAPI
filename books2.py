from fastapi import FastAPI,HTTPException,Request,status, Form, Header
from pydantic import BaseModel,Field
import uuid 
from typing import Optional
from starlette.responses import JSONResponse

app = FastAPI()



class NegativeNumberException(Exception):
    def __init__(self,books_to_return):
        self.books_to_return = books_to_return


class Book(BaseModel):
    id: uuid.UUID
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    description : Optional[str] = Field(title = " description of book",
                               min_length=5, max_length=500)
    rating : int = Field(title = "rating of book",gt=0, lt=6)

    class Config : 
        schema_extra = {
            "example": {
                "id": "f0f8f8f8-f8f8-f8f8-f8f8-f8f8f8f8f8f8",
                "title": "Book 1",
                "author": "Author 1",
                "description": "This is a book",
                "rating": 5
            }
        }

Books = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request, exceptioon:NegativeNumberException):
    return JSONResponse(content = {"error": f"hey why do you want to return {exceptioon.books_to_return} books?"}
     ,status_code=400)

@app.get("/")
async def read_all_books(books_to_returb: Optional[int] = None):
    if books_to_returb and books_to_returb < 0:
        raise NegativeNumberException(books_to_returb)
    if len(Books) == 0:
        create_books_no_api()
    
    if books_to_returb and len(Books) >= books_to_returb > 0:
        return Books[:books_to_returb]
    return Books



@app.post("/create",status_code= status.HTTP_201_CREATED)
async def create_book(book: Book):
    Books.append(book)
    return book


def create_books_no_api():
    book_1 = Book(id=uuid.uuid4(), title="Book 1", author="Author 1",description="description of book 1",rating=1)
    book_2 = Book(id=uuid.uuid4(), title="Book 2", author="Author 2",description="description of book 2",rating=2)
    book_3 = Book(id=uuid.uuid4(), title="Book 3", author="Author 3",description="description of book 3",rating=3)
    book_4 = Book(id=uuid.uuid4(), title="Book 4", author="Author 4",description="description of book 4",rating=4)
    book_5 = Book(id=uuid.uuid4(), title="Book 5", author="Author 5",description="description of book 5",rating=5)
    Books.append(book_1)
    Books.append(book_2)
    Books.append(book_3)
    Books.append(book_4)
    Books.append(book_5)

@app.get('/books/{book_id}')
async def read_book(book_id :uuid.UUID):
    for book in Books:
        if book.id == book_id:
            return book
    return {"message": "Book not found"}

@app.put('/books/{book_id}')
async def update_book(book_id :uuid.UUID, book: Book):
    for book_index in range(len(Books)):
        if Books[book_index].id == book_id:
            Books[book_index] = book
            return book


@app.delete('/books/{book_id}')
async def delete_book(book_id :uuid.UUID):
    for book_index in range(len(Books)):
        if Books[book_index].id == book_id:
            Books.pop(book_index)
            return {"message": "Book deleted"}
    
    raise raise_item_cannot_be_found_exception()



def raise_item_cannot_be_found_exception():
    raise HTTPException(status_code=404, detail="Book not found",header={"X_Header_Error": "Nothing found"})



class BookNoRating(BaseModel):
    id: uuid.UUID
    title: str = Field(min_length=1, max_length=50)
    author: str = Field(min_length=1, max_length=50)
    description : Optional[str] = Field(None,title = " description of book",min_length=5, max_length=500)


@app.get("/books/{book_id}/no_rating",response_model=BookNoRating)
async def read_book_no_rating(book_id :uuid.UUID):
    for book in Books:
        if book.id == book_id:
            return book
    raise raise_item_cannot_be_found_exception()




@app.post("/books/login")
async def book_login(username: str = Form(...), password: str = Form(...)):
    return {"username": username, "password": password}


@app.get("/header")
async def get_header(random_header: Optional[str] = Header(None)):
    return {"random_header": random_header}


@app.post("/book/login")
async def book_login( username: Optional[str] = Header(None), password: Optional[str] = Header(None)):
    if username == 'first' and password == 'first':
        return {"username": username, "password": password}
    return "Invalid User"