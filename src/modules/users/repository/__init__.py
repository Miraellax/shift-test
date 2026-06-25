import os
from contextlib import asynccontextmanager

import dotenv

from .base_repository import BaseUsersRepository
from .file_repository import FileUsersRepository
from .sqlalchemy_repository import SqlalchemyUsersRepository
from ...database import get_db

dotenv.load_dotenv()

@asynccontextmanager
async def get_sqlalchemy_users_repository():
    async with get_db() as session:
        yield SqlalchemyUsersRepository(session)

def get_file_users_repository(path = os.getenv("FILE_DB_PATH")):
    return FileUsersRepository(path)

async def get_users_repository() -> BaseUsersRepository:
    mode = os.getenv("DB_MODE")
    if mode == "postgres":
        async with get_sqlalchemy_users_repository() as repository:
            yield repository
    elif mode == "file":
        yield get_file_users_repository()
    else:
        raise Exception(f"Режим {mode} не поддерживается")
