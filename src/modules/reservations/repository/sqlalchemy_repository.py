from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ...db_models.models import Reservation
from ...exceptions import DuplicateItemValueException, ItemNotFoundException
from .base_repository import BaseReservationsRepository
from .schema import ReservationCreate as ReservationCreateSchema

class SqlalchemyReservationsRepository(BaseReservationsRepository):
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_all_reservations(self) -> Sequence[Reservation]:
        q = select(Reservation)

        return (await self.db.execute(q)).scalars().all()

    async def get_all_reservations_by_user_id(self, user_id: int) -> Sequence[Reservation]:
        q = select(Reservation).filter(Reservation.user_id == user_id)

        return (await self.db.execute(q)).scalars().all()

    async def get_reservation_info(self, reservation_id: int) -> Reservation | None:
        q = select(Reservation).filter(Reservation.id == reservation_id)

        return (await self.db.execute(q)).scalar()

    async def post_reservation(self, reservation: ReservationCreateSchema) -> Reservation:
        reservation_model = Reservation(user_id=reservation.user_id,
                                        slot_id=reservation.slot_id)
        self.db.add(reservation_model)

        try:
            await self.db.commit()
            await self.db.refresh(reservation_model)
            return reservation_model
        except IntegrityError:
            raise DuplicateItemValueException

    async def delete_reservation_by_id(self, reservation_id: int):
        reservation = await self.db.get(Reservation, reservation_id)

        if reservation is not None:
            await self.db.delete(reservation)
            await self.db.commit()
        else:
            raise DuplicateItemValueException

    async def delete_reservation_by_id_with_user(self, reservation_id: int, user_id: int):
        q = select(Reservation).filter(Reservation.id == reservation_id).filter(Reservation.user_id == user_id)
        reservation = (await self.db.execute(q)).scalar()

        if reservation is not None:
            await self.db.delete(reservation)
            await self.db.commit()
        else:
            raise ItemNotFoundException

