import sys 
sys.path.append('..')

from typing import Optional
from fastapi import APIRouter, Depends,HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import * 

router = APIRouter(
    prefix = '/address',
    tags = ['address'],
    responses = {404: {'description': 'Not found'}},
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        

class Adress(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str
    
@router.post('/')
async def create_address(address: Adress,
                         user:dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if user is None : 
        raise HTTPException(status_code=400, detail="User not found")
    
    new_address = models.Address(**address.dict())
    db.add(new_address)
    db.flush()
    user_model = db.query(models.User).filter(models.User.id == user['user_id']).first()
    user_model.address_id = new_address.id
    db.add(user_model)
    db.commit()
    # db.commit()
    db.refresh(new_address)
    return new_address