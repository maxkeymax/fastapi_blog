from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
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


async def delete(id: int, db: AsyncSession):
    result = await db.execute(
        delete(models.Blog).where(models.Blog.id == id)
    )
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} not found'
        )
    
    await db.commit()
    return {'message': f'Blog with id {id} has been deleted successfully'}


async def update(id: int, request: schemas.Blog, db: AsyncSession):
    result = await db.execute(
        select(models.Blog).where(models.Blog.id == id)
    )
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} not found'
        )
    
    blog.title = request.title
    blog.body = request.body
    
    await db.commit()
    await db.refresh(blog)
    return {'message': 'updated', 'blog': blog}


async def show(id: int, db: AsyncSession):
    result = await db.execute(
        select(models.Blog).where(models.Blog.id == id)
    )
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with id {id} is not available'
        )
    return blog
