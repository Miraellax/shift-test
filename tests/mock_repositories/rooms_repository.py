from src.modules.exceptions import DuplicateItemValueException, ItemNotFoundException
from src.modules.rooms.repository import BaseRoomsRepository
from src.modules.rooms.repository.schema import Room, RoomInfo
from src.modules.slots.repository.schema import Slot

class MockRoomsRepository(BaseRoomsRepository):
    async def get_all_rooms(self):
        return [
            Room.model_validate({
                "name": "Test_room_1",
                "id": 1
            }),
            Room.model_validate({
                "name": "Test_room_2",
                "id": 2
            })
        ]

    async def get_room_by_id(self, room_id: int):
        if room_id == 1:
            return Room.model_validate({
                        "name": "Test_room_1",
                        "id": 1
            })
        else:
            return None

    async def get_room_slots(self, room_id: int):
        if room_id == 1:
            return [
                Slot.model_validate({
                    "id": "1",
                    "room_id": "1",
                    "start_time": "10:00:00",
                    "end_time": "10:50:00",
                    "slot_date": "2026-06-18"
                }),
                Slot.model_validate({
                    "id": "2",
                    "room_id": "1",
                    "start_time": "11:00:00",
                    "end_time": "11:50:00",
                    "slot_date": "2026-06-18"
                })
            ]
        else:
            return None

    async def post_room(self, room):
        return Room.model_validate({
                    "name": "Test_room_1",
                    "id": 4
        })

    async def update_room_name(self, room_id: int, new_room_name: str):
        if new_room_name == "duplicate":
            raise DuplicateItemValueException
        elif room_id == -1:
            raise ItemNotFoundException
        else:
            return Room.model_validate({
                        "name": "Test_room_1",
                        "id": 4
            })

    async def delete_room_by_id(self, room_id: int):
        if room_id == -1:
            raise ItemNotFoundException
        else:
            return None