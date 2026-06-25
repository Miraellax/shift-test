from datetime import time, date
from typing import List

from pydantic import BaseModel, ConfigDict


class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int

    model_config = ConfigDict(
        from_attributes = True
    )


class RoomSlotInfo(BaseModel):
    start_time: time
    end_time: time
    slot_date: date

class RoomInfo(Room):
    slots: List[RoomSlotInfo]