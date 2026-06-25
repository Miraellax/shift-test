from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repository import BaseUsersRepository
from ...db_models.models import Reservation, User
from .schema import UserCreate as UserCreateSchema

class SqlalchemyUsersRepository(BaseUsersRepository):
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_all_users(self) -> Sequence[User]:
        q = select(User)

        return (await self.db.execute(q)).scalars().all()

    async def get_user_info(self, user_id: int) -> User | None:
        q = select(User).filter(User.id == user_id)

        return (await self.db.execute(q)).scalar()

    async def get_user_info_by_username(self, user_username: str) -> User | None:
        q = select(User).filter(User.username == user_username)

        return (await self.db.execute(q)).scalar()

    async def get_user_reservations(self, user_id: int) -> Sequence[Reservation]:
        q = select(Reservation).filter(Reservation.user_id == user_id)

        return (await self.db.execute(q)).scalars().all()

    async def post_user(self, user: UserCreateSchema) -> User:
        user_model = User(username=user.username,
                          hashed_password=user.hashed_password,
                          is_admin=user.is_admin)
        self.db.add(user_model)
        await self.db.commit()
        await self.db.refresh(user_model)

        return user_model
