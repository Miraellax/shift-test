from pydantic import BaseModel, ConfigDict
from datetime import date, time


class ReservationBase(BaseModel):
    user_id: int
    slot_id: int

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int

    model_config = ConfigDict(
        from_attributes = True
    )

class ReservationInfo(ReservationBase):
    slot_owner_username: str
    slot_room_name: str
    slot_date: date
    slot_start_time: time
    slot_end_time: time
