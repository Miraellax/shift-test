import os
from contextlib import asynccontextmanager

import dotenv

from .base_repository import BaseRoomsRepository
from .file_repository import FileRoomsRepository
from .sqlalchemy_repository import SqlalchemyRoomsRepository
from ...database import get_db

dotenv.load_dotenv()

@asynccontextmanager
async def get_sqlalchemy_rooms_repository():
    async with get_db() as session:
        yield SqlalchemyRoomsRepository(session)

def get_file_rooms_repository(path = os.getenv("FILE_DB_PATH")):
    return FileRoomsRepository(path)

async def get_rooms_repository() -> BaseRoomsRepository:
    mode = os.getenv("DB_MODE")
    if mode == "postgres":
        async with get_sqlalchemy_rooms_repository() as repository:
            yield repository
    elif mode == "file":
        yield get_file_rooms_repository()
    else:
        raise Exception(f"Режим {mode} не поддерживается")