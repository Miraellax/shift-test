from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from .repository import BaseSlotsRepository, get_slots_repository, schema as slots_schema
from ..auth.router import get_current_user
from ..exceptions import ItemNotFoundException
from ..rooms.repository import BaseRoomsRepository, get_rooms_repository
from ..users.repository import schema as users_schema

router = APIRouter(prefix="/slots", tags=["Slots"])

@router.get("/", response_model=Sequence[slots_schema.Slot], dependencies=[Depends(get_current_user)])
async def get_slots(slots_repo: Annotated[BaseSlotsRepository, Depends(get_slots_repository)]
                    ) -> Sequence[slots_schema.Slot]:
    result = await slots_repo.get_all_slots()

    return result

@router.get("/{slot_id}", response_model=slots_schema.SlotInfo, dependencies=[Depends(get_current_user)])
async def get_slot_info(slot_id: int,
                        slots_repo: Annotated[BaseSlotsRepository, Depends(get_slots_repository)],
                        rooms_repo: Annotated[BaseRoomsRepository, Depends(get_rooms_repository)]
                        ) -> slots_schema.SlotInfo:
    slot = await slots_repo.get_slot_info(slot_id)
    if slot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Слот не найден")

    slot_room = await rooms_repo.get_room_by_id(slot.room_id)
    if slot_room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Комната не найдена")

    slot_reservations = await slots_repo.get_slot_reservation(slot_id)

    slot_info = slots_schema.SlotInfo(room_id=slot.room_id,
                                      start_time=slot.start_time,
                                      end_time=slot.end_time,
                                      slot_date=slot.slot_date,
                                      room_name=slot_room.name,
                                      is_reserved=(slot_reservations is not None))

    return slot_info


@router.post("/", response_model=slots_schema.Slot)
async def post_slot(slot: slots_schema.SlotCreate,
                    current_user: Annotated[users_schema.User, Depends(get_current_user)],
                    slots_repo: Annotated[BaseSlotsRepository, Depends(get_slots_repository)],
                    rooms_repo: Annotated[BaseRoomsRepository, Depends(get_rooms_repository)]
                    ) -> slots_schema.Slot:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="У вас нет прав для создания слотов")

    # Проверка на корректность начала/конца времени слота реализована в slots_schema.Slot
    # Проверка, что нужная для слота комната существует
    room = await rooms_repo.get_room_by_id(slot.room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Комната не найдена")

    result = await slots_repo.post_slot(slot)

    return slots_schema.Slot.model_validate(result)

@router.delete("/{slot_id}", response_model=None)
async def delete_slot_by_id(slot_id: int,
                            current_user: Annotated[users_schema.User, Depends(get_current_user)],
                            slots_repo: Annotated[BaseSlotsRepository, Depends(get_slots_repository)]
                            ):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="У вас нет прав для удаления слотов")
    try:
        await slots_repo.delete_slot_by_id(slot_id)
    except ItemNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Слот не найден")
