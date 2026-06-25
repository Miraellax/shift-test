import os
from contextlib import asynccontextmanager

import dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


dotenv.load_dotenv()
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_NAME")

# Async PostgreSQL DB
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=True)
session_maker = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_db():
    async with session_maker() as session:
        yield session