from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import models


class CreateUser(BaseModel):
    username: str
    password: str
    email: Optional[str]
    first_name: str
    last_name: str


app = FastAPI()


@app.post("/create/users")
async def create_user(user: CreateUser):
    users = models.User()
    users.username = user.username
    users.hashed_password = user.password
    users.email = user.email
    users.first_name = user.first_name
    users.last_name = user.last_name
    users.is_active = True
    return user