from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, models, token
from ..database import get_async_db
from ..hashing import Hash

router = APIRouter(
    tags=['login']
)

@router.post('/login')
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    result = await db.execute(models.User.__table__.select().where(models.User.email == request.username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid Credentials'
        )

    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect password'
        )

    access_token = token.create_access_token(data={"sub": user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}