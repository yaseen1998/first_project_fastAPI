from fastapi import FastAPI,Depends,HTTPException
from database import Base,engine,SessionLocal
import models
from typing import Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try :
         db = SessionLocal()
         yield db
    finally:
        db.close()


# @app.get("/")
# async def create_database():
#     return {"message": "Hello World"}

class Todo(BaseModel):
    title: str
    completed: bool
    description : Optional[str] 
    priority : int = Field(gt=0, lt=5,description = "Priority must be between 1 and 5")
    # created_at : Optional[str] = Field(description = "Format: YYYY-MM-DD HH:MM:SS")

@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()

@app.post("/")
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    db_todo = models.Todos()
    db_todo.title = todo.title
    db_todo.completed = todo.completed
    db_todo.description = todo.description
    db_todo.priority = todo.priority
    db.add(db_todo)
    db.commit()
    return {"status":201,"message":"Todo created successfully"}


@app.put("/{todo_id}")
async def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todos).get(todo_id)
    if not db_todo:
        raise http_exsception()
    db_todo.title = todo.title
    db_todo.completed = todo.completed
    db_todo.description = todo.description
    db_todo.priority = todo.priority
    db.commit()
    return {"status":200,"message":"Todo updated successfully"}

@app.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todos).get(todo_id)
    if not db_todo:
        raise http_exsception()
    db.delete(db_todo)
    db.commit()
    return {"status":200,"message":"Todo deleted successfully"}

@app.get("/{id}")
async def read_one(id: int, db: Session = Depends(get_db)):
    todo =  db.query(models.Todos).filter(models.Todos.id == id).first()
    if todo is None:
        raise http_exsception()
    return todo

def http_exsception():
    return HTTPException(status_code=404, detail="Not found")