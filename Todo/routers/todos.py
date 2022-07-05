import sys 
sys.path.append('..')

from starlette.responses import RedirectResponse
from starlette import status

from fastapi import FastAPI,Depends,HTTPException,APIRouter,Request, Form
from database import Base,engine,SessionLocal
import models
from typing import Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from .auth import get_current_user


from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

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
        
        
@router.get("/",response_class=HTMLResponse)
async def read_all_by_user(request:Request,db:Session=Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get('user_id')).all()
    return templates.TemplateResponse("home.html",{'request':request,'todos' : todos})

@router.get("/add",response_class=HTMLResponse)
async def add_todo(request:Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("todo.html",{'request':request})


@router.post("/add",response_class=HTMLResponse)
async def add_todos(request:Request,
                    title:str=Form(...),
                    description:str=Form(...),
                    priority:int=Form(...),
                    db:Session=Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todo = models.Todos(
        title = title,
        description = description,
        owner_id = user.get('user_id'),
        priority = priority
        # priority = request.form.get("priority")
    )
    db.add(todo)
    db.commit()
    return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)


@router.get("/edit/{todo_id}",response_class=HTMLResponse)
async def edit_todos(request:Request,todo_id:int,db:Session=Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todo = db.query(models.Todos).get(todo_id)
    print(todo)
    return templates.TemplateResponse("edit.html",{'request':request,'todo' : todo})



@router.post("/edit/{todo_id}",response_class=HTMLResponse)
async def edit_todo(request:Request,
                    todo_id:int,
                    title:str=Form(...),
                    description:str=Form(...),
                    priority:int=Form(...),
                    db:Session=Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todo = db.query(models.Todos).get(todo_id)
    todo.title = title
    todo.description = description
    todo.priority = priority
    db.add(todo)
    db.commit()
    return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)


@router.get("/delete/{todo_id}",response_class=HTMLResponse)
async def delete_todo(request:Request,todo_id:int,db:Session=Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todo = db.query(models.Todos).get(todo_id)
    if todo is None :
        return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)

    db.delete(todo)
    db.commit()
    return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)


@router.get("/complete/{todo_id}",response_class=HTMLResponse)
async def complete_todo(request:Request,todo_id:int,db:Session=Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todo = db.query(models.Todos).get(todo_id)
    todo.completed = not todo.completed
    db.add(todo)
    db.commit()
    return RedirectResponse(url="/todos",status_code=status.HTTP_302_FOUND)
#
# @router.get("/")
# async def create_database():
#     return {"message": "Hello World"}

# class Todo(BaseModel):
#     title: str
#     completed: bool
#     description : Optional[str] 
#     priority : int = Field(gt=0, lt=5,description = "Priority must be between 1 and 5")
#     # created_at : Optional[str] = Field(description = "Format: YYYY-MM-DD HH:MM:SS")

# @router.get('/test')
# async def test(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})

# @router.get("/")
# async def read_all(db: Session = Depends(get_db)):
#     return db.query(models.Todos).all()


# @router.get("/todo/user")
# async def readd_all_by_user(user:dict = Depends(get_current_user),db: Session = Depends(get_db)):
#     if user is None :
#         raise http_exsception()
#     print(user)
#     return db.query(models.Todos).filter(models.Todos.owner_id == user.get('user_id')).all()

# @router.post("/")
# async def create_todo(todo: Todo,user:dict= Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None :
#         raise http_exsception()
#     db_todo = models.Todos()
#     db_todo.title = todo.title
#     db_todo.completed = todo.completed
#     db_todo.description = todo.description
#     db_todo.priority = todo.priority
#     db_todo.owner_id = user.get('user_id')
#     db.add(db_todo)
#     db.commit()
#     return {"status":201,"message":"Todo created successfully"}


# @router.put("/{todo_id}")
# async def update_todo(todo_id: int, todo: Todo,user:dict= Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None :
#         raise http_exsception()
#     db_todo = db.query(models.Todos).filter(models.Todos.owner_id == user.get('user_id') ).filter(models.Todos.id == todo_id).first()
#     if not db_todo:
#         raise http_exsception()
#     db_todo.title = todo.title
#     db_todo.completed = todo.completed
#     db_todo.description = todo.description
#     db_todo.priority = todo.priority
#     db.commit()
#     return {"status":200,"message":"Todo updated successfully"}

# @router.delete("/{todo_id}")
# async def delete_todo(todo_id: int,user:dict= Depends(get_current_user), db: Session = Depends(get_db)):
#     print(user)
#     if user is None :
#         raise http_exsception()
#     # db_todo = db.query(models.Todos).get(todo_id)
#     db_todo = db.query(models.Todos).filter(models.Todos.owner_id == user.get('user_id') ).filter(models.Todos.id == todo_id).first()

#     if not db_todo:
#         raise http_exsception()
#     db.delete(db_todo)
#     db.commit()
#     return {"status":200,"message":"Todo deleted successfully"}

# @router.get("/{id}")
# async def read_one(id: int,user:dict= Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None :
#         raise http_exsception()
#     todo =  db.query(models.Todos).filter(models.Todos.id == id).filter(models.Todos.owner_id == user.get('user_id')).first()
#     if todo is None:
#         raise http_exsception()
#     return todo

# def http_exsception():
#     return HTTPException(status_code=404, detail="Not found")