from abc import abstractmethod
from typing import Sequence

from .schema import Room as RoomSchema, RoomCreate as RoomCreateSchema
from ...slots.repository.schema import Slot as SlotSchema


class BaseRoomsRepository:
    @abstractmethod
    async def get_all_rooms(self) -> Sequence[RoomSchema]:
        pass

    @abstractmethod
    async def get_room_by_id(self, room_id: int) -> RoomSchema | None:
        pass

    @abstractmethod
    async def get_room_slots(self, room_id: int) -> Sequence[SlotSchema]:
        pass

    @abstractmethod
    async def post_room(self, room: RoomCreateSchema) -> RoomSchema:
        pass

    @abstractmethod
    async def update_room_name(self, room_id: int, new_room_name: str) -> RoomSchema:
        pass

    @abstractmethod
    async def delete_room_by_id(self, room_id: int):
        pass