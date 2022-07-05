from re import template
import sys 
sys.path.append('..')
from fastapi import FastAPI , Depends, HTTPException, APIRouter, Request,status,Response,Form
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from database import SessionLocal , engine
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from jose import jwt , JWTError
from starlette.responses import RedirectResponse

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")

class CreateUser(BaseModel):
    username: str
    password: str
    email: Optional[str]
    first_name: str
    last_name: str


dcrypt_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

pauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")

# router = FastAPI()
router = APIRouter(
     prefix="/auth",
    tags = ["auth"],
    responses = {404:{'user':'unauthorized'}}

)

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


async def get_current_user(request: Request):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id = int = payload.get("user_id")
        if username is None or user_id is None:
            raise credentials_exception
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise credentials_exception


@router.post("/create/users")
async def create_user(user: CreateUser,db : Session = Depends(get_db)):
    users = models.User()
    users.username = user.username
    users.hashed_password = get_password_hash(user.password)
    # users.hashed_password = user.password
    users.email = user.email
    users.first_name = user.first_name
    users.last_name = user.last_name
    users.is_active = True
    db.add(users)
    db.commit()

    return users

@router.post("/token")
async def login_for_aaccess_token(response:Response,form_data: OAuth2PasswordRequestForm  = Depends(),db : Session = Depends(get_db)):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(user.username,user.id,expires_delta =   access_token_expires)
    response.set_cookie(key="access_token",value=access_token,max_age=access_token_expires,httponly=True)
    return True


@router.get("/", response_class=HTMLResponse)
async def authpage(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@router.get("/register/", response_class=HTMLResponse)
async def authpage(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register/", response_class=HTMLResponse)
async def register_user(request: Request,email:str=Form(...),
                        username:str=Form(...),
                   password:str=Form(...),confirm_password:str=Form(...),
                   first_name:str=Form(...),last_name:str=Form(...),
                        db:Session=Depends(get_db)):
    validate = db.query(models.User).filter(models.User.username == username).first()
    valdiate2 = db.query(models.User).filter(models.User.email == email).first()
    
    if password != confirm_password or validate is not None or valdiate2 is not None:
        print("validate",validate)
        print("valdiate2",valdiate2)
        return templates.TemplateResponse("register.html", {"request": request,"error":"Passwords do not match"})
    user = models.User()
    user.username = username
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.hashed_password = get_password_hash(password)
    user.is_active = True
    user.phone_number = 'phone_number'
    db.add(user)
    db.commit()
    
    return templates.TemplateResponse("login.html", {"request": request})
    
class LoginForm:
    def __init__(self,request: Request):
        self.request : Request = request
        self.username : Optional[str] = None
        self.password : Optional[str] = None
        
    async def create_auth_form(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
        
@router.post("/", response_class=HTMLResponse)
async def login(request:Request,db : Session = Depends(get_db)):
    form = LoginForm(request)
    await form.create_auth_form()
    response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
    validate_user_cookie = await login_for_aaccess_token(response,form_data=form,db=db)
    
    if validate_user_cookie:
        return response
    msg = "Incorrect username or password"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})

@router.get("/logout")
async def logout(request: Request):
    msg = "You have been logged out"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie("access_token")
    return response