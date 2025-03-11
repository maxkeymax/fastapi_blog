from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from .. import models, schemas


async def get_all(db: AsyncSession):
    result = await db.execute(models.Blog.select())
    return result.scalars().all()

async def create(request: schemas.Blog, db: AsyncSession):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog

async def delete(id, db: AsyncSession):
    result = await db.execute(
        models.Blog.select().where(models.Blog.id == id)
    )
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} not found'
        )
    await db.delete(blog)
    await db.commit()
    return 'done'

async def update(id, request: schemas.Blog, db: AsyncSession):
    result = await db.execute(
        models.Blog.select().where(models.Blog.id == id)
    )
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} not found'
        )
    blog.update(request.model_dump())
    await db.commit()
    return 'updated'

async def show(id, db: AsyncSession):
    result = await db.execute(
        models.Blog.select().where(models.Blog.id == id)
    )
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} is not available'
        )
    return blog