from abc import abstractmethod
from typing import Sequence

from ...db_models.models import Slot, Reservation
from .schema import SlotCreate as SlotCreateSchema


class BaseSlotsRepository:
    @abstractmethod
    async def get_all_slots(self) -> Sequence[Slot]:
        pass

    @abstractmethod
    async def get_slot_info(self, slot_id: int) -> Slot | None:
        pass

    @abstractmethod
    async def get_slot_reservation(self, slot_id: int) -> Reservation | None:
        pass

    @abstractmethod
    async def post_slot(self, room: SlotCreateSchema) -> Slot:
        pass

    @abstractmethod
    async def delete_slot_by_id(self, slot_id: int):
        pass