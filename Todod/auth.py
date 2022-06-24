from fastapi import FastAPI , Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from database import SessionLocal , engine
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from jose import jwt , JWTError


SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

class CreateUser(BaseModel):
    username: str
    password: str
    email: Optional[str]
    first_name: str
    last_name: str


dcrypt_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

pauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI()

def get_db():
    try :
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return dcrypt_ctx.hash(password)


def verify_password(plain_password, hashed_password):
    return dcrypt_ctx.verify(plain_password, hashed_password)


def authenticate_user(username:str,password: str,db):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id: int,expires_delta: Optional[timedelta] = None):
    encode = {"username": username, "user_id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else :
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})

    token = jwt.encode(
        encode, SECRET_KEY, algorithm=ALGORITHM
    )
    # return token.decode("utf-8")
    return token


async def get_current_user(token: str = Depends(pauth2_bearer)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id = int = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise credentials_exception


@app.post("/create/users")
async def create_user(user: CreateUser,db : Session = Depends(get_db)):
    users = models.User()
    users.username = user.username
    # users.hashed_password = get_password_hash(user.password)
    users.hashed_password = user.password
    users.email = user.email
    users.first_name = user.first_name
    users.last_name = user.last_name
    users.is_active = True
    db.add(users)
    db.commit()

    return users

@app.post("/token")
async def login_for_aaccess_token(form_data: OAuth2PasswordRequestForm  = Depends(),db : Session = Depends(get_db)):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(user.username,user.id,expires_delta =   access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
