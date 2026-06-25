import json
from typing import Sequence

from .schema import User as UserSchema, UserCreate as UserCreateSchema
from modules.reservations.repository.schema import Reservation as ReservationSchema
from .base_repository import BaseUsersRepository


class FileUsersRepository(BaseUsersRepository):
    def __init__(self, path):
        self.path = path
        self.indent = 4

    def write_file(self, data):
        with open(self.path, "w") as file:
            json.dump(obj=data, fp=file, indent=self.indent)

    def read_file(self) -> dict:
        with open(self.path, "r") as file:
            return json.load(file)

    async def get_all_users(self) -> Sequence[UserSchema]:
        pass

    async def get_user_info(self, user_id: int) -> UserSchema | None:
        pass

    async def get_user_info_by_username(self, user_username: str) -> UserSchema | None:
        pass

    async def get_user_reservations(self, user_id: int) -> Sequence[ReservationSchema]:
        pass

    async def post_user(self, user: UserCreateSchema) -> UserSchema:
        pass