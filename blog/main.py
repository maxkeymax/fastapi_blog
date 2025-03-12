from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import async_engine, Base
from .routers import blog, user, authentication

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)


app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)