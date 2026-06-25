import os
from contextlib import asynccontextmanager

import dotenv

from .base_repository import BaseReservationsRepository
from .file_repository import FileReservationsRepository
from .sqlalchemy_repository import SqlalchemyReservationsRepository
from ...database import get_db

dotenv.load_dotenv()

@asynccontextmanager
async def get_sqlalchemy_reservations_repository():
    async with get_db() as session:
        yield SqlalchemyReservationsRepository(session)

def get_file_reservations_repository(path = os.getenv("FILE_DB_PATH")):
    return FileReservationsRepository(path)

async def get_reservations_repository() -> BaseReservationsRepository:
    mode = os.getenv("DB_MODE")
    if mode == "postgres":
        async with get_sqlalchemy_reservations_repository() as repository:
            yield repository
    elif mode == "file":
        yield get_file_reservations_repository()
    else:
        raise Exception(f"Режим {mode} не поддерживается")