from datetime import date, time

from pydantic import BaseModel, model_validator, ConfigDict


class SlotBase(BaseModel):
    room_id: int
    start_time: time
    end_time: time
    slot_date: date

    @model_validator(mode="after")
    def validate_end_time(self):
        if self.start_time >= self.end_time:
            raise ValueError("Время окончания слота должно быть позже времени начала слота")
        return self

class SlotCreate(SlotBase):
    pass

class Slot(SlotBase):
    id: int

    model_config = ConfigDict(
        from_attributes = True
    )

class SlotInfo(SlotBase):
    room_name: str
    is_reserved: bool