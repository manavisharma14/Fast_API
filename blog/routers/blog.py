from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, models, database
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
)

get_db = database.get_db



@router.get('/', response_model=list[schemas.ShowBlog])
def all(db : Session = Depends(get_db)):
    return blog.get_all(db)
    


@router.post('/', response_model=schemas.ShowBlog)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)





@router.delete('/{id}', status_code=status.HTTP_200_OK)
def destroy(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id, db)



@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db : Session = Depends(get_db)):
    return blog.update(id, request, db)

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def show(id, response: Response, db : Session = Depends(get_db)):
    return blog.show(id, db)



