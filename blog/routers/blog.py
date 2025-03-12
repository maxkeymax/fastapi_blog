from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import oauth2, schemas
from ..database import get_async_db
from ..repository import blog

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)

@router.get('/', response_model=List[schemas.ShowBlog])
async def all(
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return await blog.get_all(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create(
    request: schemas.Blog,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return await blog.create(request, db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return await blog.delete(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update(
    id: int,
    request: schemas.Blog,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return await blog.update(id, request, db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def show(
    id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: schemas.User = Depends(oauth2.get_current_user)
):
    blog_data = await blog.show(id, db)
    if not blog_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} not found"
        )
    return blog_data