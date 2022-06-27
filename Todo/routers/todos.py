import sys 
sys.path.append('..')


from fastapi import FastAPI,Depends,HTTPException,APIRouter
from database import Base,engine,SessionLocal
import models
from typing import Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from .auth import get_current_user


router = APIRouter(
     prefix="/todos",
    tags = ["todos"],
    responses = {404:{'desctiption':'not found'}}

)
models.Base.metadata.create_all(bind=engine)


def get_db():
    try :
         db = SessionLocal()
         yield db
    finally:
        db.close()


# @router.get("/")
# async def create_database():
#     return {"message": "Hello World"}

class Todo(BaseModel):
    title: str
    completed: bool
    description : Optional[str] 
    priority : int = Field(gt=0, lt=5,description = "Priority must be between 1 and 5")
    # created_at : Optional[str] = Field(description = "Format: YYYY-MM-DD HH:MM:SS")

@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@router.get("/todo/user")
async def readd_all_by_user(user:dict = Depends(get_current_user),db: Session = Depends(get_db)):
    if user is None :
        raise http_exsception()
    print(user)
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get('user_id')).all()

@router.post("/")
async def create_todo(todo: Todo,user:dict= Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None :
        raise http_exsception()
    db_todo = models.Todos()
    db_todo.title = todo.title
    db_todo.completed = todo.completed
    db_todo.description = todo.description
    db_todo.priority = todo.priority
    db_todo.owner_id = user.get('user_id')
    db.add(db_todo)
    db.commit()
    return {"status":201,"message":"Todo created successfully"}


@router.put("/{todo_id}")
async def update_todo(todo_id: int, todo: Todo,user:dict= Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None :
        raise http_exsception()
    db_todo = db.query(models.Todos).filter(models.Todos.owner_id == user.get('user_id') ).filter(models.Todos.id == todo_id).first()
    if not db_todo:
        raise http_exsception()
    db_todo.title = todo.title
    db_todo.completed = todo.completed
    db_todo.description = todo.description
    db_todo.priority = todo.priority
    db.commit()
    return {"status":200,"message":"Todo updated successfully"}

@router.delete("/{todo_id}")
async def delete_todo(todo_id: int,user:dict= Depends(get_current_user), db: Session = Depends(get_db)):
    print(user)
    if user is None :
        raise http_exsception()
    # db_todo = db.query(models.Todos).get(todo_id)
    db_todo = db.query(models.Todos).filter(models.Todos.owner_id == user.get('user_id') ).filter(models.Todos.id == todo_id).first()

    if not db_todo:
        raise http_exsception()
    db.delete(db_todo)
    db.commit()
    return {"status":200,"message":"Todo deleted successfully"}

@router.get("/{id}")
async def read_one(id: int,user:dict= Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None :
        raise http_exsception()
    todo =  db.query(models.Todos).filter(models.Todos.id == id).filter(models.Todos.owner_id == user.get('user_id')).first()
    if todo is None:
        raise http_exsception()
    return todo

def http_exsception():
    return HTTPException(status_code=404, detail="Not found")