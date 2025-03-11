from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from .. import models, schemas, database
from ..hashing import Hash

async def create(request: schemas.User, db: AsyncSession):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def show(id: int, db: AsyncSession):
    result = await db.execute(
        models.User.select().where(models.User.id == id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User {id} not found'
        )
    return user