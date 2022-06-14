from fastapi import FastAPI
from database import Base,engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def create_database():
    return {"message": "Hello World"}