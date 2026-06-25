from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseSlotsRepository
from ...db_models.models import Slot, Reservation
from .schema import SlotCreate as SlotCreateSchema
from ...exceptions import ItemNotFoundException

class SqlalchemySlotsRepository(BaseSlotsRepository):
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_all_slots(self) -> Sequence[Slot]:
        q = select(Slot)

        return (await self.db.execute(q)).scalars().all()

    async def get_slot_info(self, slot_id: int) -> Slot | None:
        q = select(Slot).filter(Slot.id == slot_id)

        return (await self.db.execute(q)).scalar()

    async def get_slot_reservation(self, slot_id: int) -> Reservation | None:
        q = select(Reservation).filter(Reservation.slot_id == slot_id)

        return (await self.db.execute(q)).scalar()

    async def post_slot(self, slot: SlotCreateSchema) -> Slot:
        slot_model = Slot(start_time=slot.start_time,
                          end_time=slot.end_time,
                          slot_date=slot.slot_date,
                          room_id=slot.room_id)
        self.db.add(slot_model)

        # Проверки на существование комнаты и непересекаемость слотов выполняются в эндпоинте
        await self.db.commit()
        await self.db.refresh(slot_model)

        return slot_model

    async def delete_slot_by_id(self, slot_id: int):
        slot = await self.db.get(Slot, slot_id)

        if slot is not None:
            await self.db.delete(slot)
            await self.db.commit()
        else:
            raise ItemNotFoundException