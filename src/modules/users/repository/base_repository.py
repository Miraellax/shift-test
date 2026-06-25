from abc import abstractmethod
from typing import Sequence

from ...db_models.models import User, Reservation
from .schema import UserCreate as UserCreateSchema


class BaseUsersRepository:
    @abstractmethod
    async def get_all_users(self) -> Sequence[User]:
        pass

    @abstractmethod
    async def get_user_info(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_user_info_by_username(self, user_username: str) -> User | None:
        pass

    @abstractmethod
    async def get_user_reservations(self, user_id: int) -> Sequence[Reservation]:
        pass

    @abstractmethod
    async def post_user(self, user: UserCreateSchema) -> User:
        pass
