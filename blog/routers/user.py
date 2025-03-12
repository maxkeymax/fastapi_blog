from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..repository import user
from .. import schemas
from ..database import get_async_db

router = APIRouter(
    prefix='/user',
    tags=['users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
async def create_user(request: schemas.User, db: AsyncSession = Depends(get_async_db)):
    return await user.create(request, db)

@router.get('/{id}', response_model=schemas.ShowUser)
async def get_user(id: int, db: AsyncSession = Depends(get_async_db)):
    user_data = await user.show(id, db)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
    return user_data