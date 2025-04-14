from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session

router = APIRouter()

get_db = database.get_db

@router.get('/blog', response_model=list[schemas.ShowBlog], tags=['blogs'])
def all(db : Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/blog', response_model=schemas.ShowBlog, tags=['blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title, 
        body=request.body, 
        user_id=1   # hardcode or fetch dynamically
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
