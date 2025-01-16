from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import oauth2, schemas, database, models
from ..repository import blog


router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)
get_db = database.get_db

@router.get('/', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request, db)
    


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db),
        current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id, request, db)

    
@router.get('/{id}', status_code=status.HTTP_200_OK,
         response_model=schemas.ShowBlog)
def show(id: int, db: Session = Depends(get_db),
         response_model=schemas.ShowBlog,
         current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show(id, db)