import json
from typing import Sequence

from .base_repository import BaseSlotsRepository
from .schema import Slot as SlotSchema, SlotCreate as SlotCreateSchema
from ...reservations.repository.schema import Reservation as ReservationSchema


class FileSlotsRepository(BaseSlotsRepository):
    def __init__(self, path):
        self.path = path
        self.indent = 4

    def write_file(self, data):
        with open(self.path, "w") as file:
            json.dump(obj=data, fp=file, indent=self.indent)

    def read_file(self) -> dict:
        with open(self.path, "r") as file:
            return json.load(file)

    async def get_all_slots(self) -> Sequence[SlotSchema]:
        pass

    async def get_slot_info(self, slot_id: int) -> SlotSchema | None:
        pass

    async def get_slot_reservation(self, slot_id: int) -> ReservationSchema | None:
        pass

    async def post_slot(self, room: SlotCreateSchema) -> SlotSchema:
        pass

    async def delete_slot_by_id(self, slot_id: int):
        pass