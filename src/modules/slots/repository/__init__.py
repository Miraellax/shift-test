import os
from contextlib import asynccontextmanager

import dotenv

from .base_repository import BaseSlotsRepository
from .file_repository import FileSlotsRepository
from .sqlalchemy_repository import SqlalchemySlotsRepository
from ...database import get_db

dotenv.load_dotenv()

@asynccontextmanager
async def get_sqlalchemy_slots_repository():
    async with get_db() as session:
        yield SqlalchemySlotsRepository(session)

def get_file_slots_repository(path = os.getenv("FILE_DB_PATH")):
    return FileSlotsRepository(path)

async def get_slots_repository() -> BaseSlotsRepository:
    mode = os.getenv("DB_MODE")
    if mode == "file":
        async with get_sqlalchemy_slots_repository() as repository:
            yield repository
    elif mode == "postgres":
        yield get_file_slots_repository()
    else:
        raise Exception(f"Режим {mode} не поддерживается")