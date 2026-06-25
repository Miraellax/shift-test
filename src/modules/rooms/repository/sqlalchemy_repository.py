from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseRoomsRepository
from ...db_models.models import Room, Slot
from .schema import RoomCreate as RoomCreateSchema
from ...exceptions import ItemNotFoundException, DuplicateItemValueException

class SqlalchemyRoomsRepository(BaseRoomsRepository):
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_all_rooms(self) -> Sequence[Room]:
        q = select(Room)

        return (await self.db.execute(q)).scalars().all()

    async def get_room_by_id(self, room_id: int) -> Room | None:
        q = select(Room).filter(Room.id == room_id)

        return (await self.db.execute(q)).scalar()

    async def get_room_slots(self, room_id: int) -> Sequence[Slot]:
        q = select(Slot).filter(Slot.room_id == room_id)

        return (await self.db.execute(q)).scalars().all()

    async def post_room(self, room: RoomCreateSchema) -> Room:

        room_model = Room(name=room.name)
        self.db.add(room_model)

        try:
            await self.db.commit()
            await self.db.refresh(room_model)
        except IntegrityError:
            raise DuplicateItemValueException

        return room_model

    async def update_room_name(self, room_id: int, new_room_name: str) -> Room:
        q = update(Room).where(Room.id == room_id).values(name=new_room_name).returning(Room)
        room = (await self.db.execute(q)).scalar()

        if room is not None:
            try:
                await self.db.commit()
            except IntegrityError:
                raise DuplicateItemValueException
        else:
            raise ItemNotFoundException

        return room

    async def delete_room_by_id(self, room_id: int):
        room = await self.db.get(Room, room_id)

        if room is not None:
            await self.db.delete(room)
            await self.db.commit()
        else:
            raise ItemNotFoundException