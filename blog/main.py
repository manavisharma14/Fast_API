from fastapi import FastAPI
from .database import engine, get_db
from .routers import blog, user, authentication
from . import models

app = FastAPI()




models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)



