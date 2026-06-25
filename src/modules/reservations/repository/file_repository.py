import json
from typing import Sequence

from .base_repository import BaseReservationsRepository
from .schema import Reservation as ReservationCSchema, ReservationCreate as ReservationCreateSchema



class FileReservationsRepository(BaseReservationsRepository):
    def __init__(self, path):
        self.path = path
        self.indent = 4

    def write_file(self, data):
        with open(self.path, "w") as file:
            json.dump(obj=data, fp=file, indent=self.indent)

    def read_file(self) -> dict:
        with open(self.path, "r") as file:
            return json.load(file)

    def get_all_reservations(self) -> Sequence[ReservationCSchema]:
        pass

    def get_all_reservations_by_user_id(self, user_id: int) -> Sequence[ReservationCSchema]:
        pass

    def get_reservation_info(self, reservation_id: int) -> ReservationCSchema | None:
        pass

    def post_reservation(self, reservation: ReservationCreateSchema) -> ReservationCSchema:
        pass

    def delete_reservation_by_id(self, reservation_id: int):
        pass

    def delete_reservation_by_id_with_user(self, reservation_id: int, user_id: int):
        pass