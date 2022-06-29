import sys
sys.path.append('..')

from fastapi import FastAPI, Depends,APIRouter
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import * 


router = APIRouter(
    prefix='/users',
    tags =  ['users'],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
class UserVerfications(BaseModel):
    username: str
    password: str
    new_password: str
        
@router.get('/')
async def read_all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{user_id}/')
async def read_one(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is not None:
        return user
    else :
        return 'User not found'
    

@router.get('/user/')
async def user_by_query(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is not None:
        return user
    else :
        return 'User not found'
        
        
@router.put('/user/password/')
async def user_password_update(user_verfications: UserVerfications,
                               user : dict = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    print(user)
    user = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    if user is not None:
        if user_verfications.username == user.username and verify_password(user_verfications.password,user.hashed_password):
            user.hashed_password = get_password_hash(user_verfications.new_password)
            db.add(user)
            db.commit()
            return 'Password updated'
        else:
            return 'Password incorrect'
    else:
        return 'User not found' 
                               


@router.delete('/user/')
async def user_delete(user : dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user.get('user_id')).first()
    if user is not None:
        db.delete(user)
        db.commit()
        return 'User deleted'
    else:
        return 'User not found'