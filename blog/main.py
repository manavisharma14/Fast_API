from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session
app = FastAPI()
from typing import List
from passlib.context import CryptContext
from .hashing import Hash
from .routers import blog


models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()







@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy(id, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'



@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id, request: schemas.Blog, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found!')
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return 'updated'

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def show(id, response: Response, db : Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found!')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {id} not found'}

    
    return blog




@app.post('/user', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['users'])
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with {id} not found!')
    return user