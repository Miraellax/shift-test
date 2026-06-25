import json
from typing import Sequence

from .base_repository import BaseRoomsRepository
from .schema import Room as RoomSchema, RoomCreate as RoomCreateSchema
from ...slots.repository.schema import Slot as SlotSchema

class FileRoomsRepository(BaseRoomsRepository):
    def __init__(self, path):
        self.path = path
        self.indent = 4

    def write_file(self, data):
        with open(self.path, "w") as file:
            json.dump(obj=data, fp=file, indent=self.indent)

    def read_file(self) -> dict:
        with open(self.path, "r") as file:
            return json.load(file)

    async def get_all_rooms(self) -> Sequence[RoomSchema]:
        pass

    async def get_room_by_id(self, room_id: int) -> RoomSchema | None:
        pass

    async def get_room_slots(self, room_id: int) -> Sequence[SlotSchema]:
        pass

    async def post_room(self, room: RoomCreateSchema) -> RoomSchema:
        pass

    async def update_room_name(self, room_id: int, new_room_name: str) -> RoomSchema:
        pass

    async def delete_room_by_id(self, room_id: int):
        pass