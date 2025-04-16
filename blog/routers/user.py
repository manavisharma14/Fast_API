from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, schemas, database
from sqlalchemy.orm import Session
from ..database import get_db
from ..hashing import Hash
from ..repository import user

router = APIRouter(
    tags=['Users'],
    prefix='/user'

)

@router.post('/', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)
    


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id, db: Session = Depends(get_db)):
    return user.show(id, db)