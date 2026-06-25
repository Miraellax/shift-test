from abc import abstractmethod

from .schema import ReservationCreate as ReservationCreateSchema


class BaseReservationsRepository:
    @abstractmethod
    async def get_all_reservations(self):
        pass

    @abstractmethod
    async def get_all_reservations_by_user_id(self, user_id: int):
        pass

    @abstractmethod
    async def get_reservation_info(self, reservation_id: int):
        pass

    @abstractmethod
    async def post_reservation(self, reservation: ReservationCreateSchema):
        pass

    @abstractmethod
    async def delete_reservation_by_id(self, reservation_id: int):
        pass

    @abstractmethod
    async def delete_reservation_by_id_with_user(self, reservation_id: int, user_id: int):
        pass