from fastapi import FastAPI,Depends
from database import engine
import models


from routers import auth, todos, users,address
from company import companyapi,depend
from starlette.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(address.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todos.router)
app.include_router(companyapi.router, 
                   dependencies=[Depends(depend.get_token_header)],
                   prefix='/company',
                   tags=['company'],responses={418: {"description": "Not found"}})
