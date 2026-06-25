from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from .repository import BaseRoomsRepository, get_rooms_repository, schema as rooms_schema
from ..auth.router import get_current_user
from ..exceptions import DuplicateItemValueException, ItemNotFoundException
from ..users.repository import schema as users_schema

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/", response_model=Sequence[rooms_schema.Room], dependencies=[Depends(get_current_user)])
async def get_rooms(rooms_repo: Annotated[BaseRoomsRepository, Depends(get_rooms_repository)]
                    ) -> Sequence[rooms_schema.Room]:
    result = await rooms_repo.get_all_rooms()

    return result

@router.get("/{room_id}", response_model=rooms_schema.Room, dependencies=[Depends(get_current_user)])
async def get_room_info(room_id: int,
                        rooms_repo: Annotated[BaseRoomsRepository, Depends(get_rooms_repository)]
                        ) -> Sequence[rooms_schema.Room]:
    result = await rooms_repo.get_room_by_id(room_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена")

    return result

@router.get("/{room_id}/slots", response_model=rooms_schema.RoomInfo, dependencies=[Depends(get_current_user)])
async def get_room_slots(room_id: int,
                         rooms_repo: Annotated[BaseRoomsRepository, Depends(get_rooms_repository)]
                         ) -> rooms_schema.RoomInfo:
    room = await rooms_repo.get_room_by_id(room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена")

    room_slots = await rooms_repo.get_room_slots(room_id)
    result = rooms_schema.RoomInfo(
        id=room.id,
        name=room.name,
        slots=[rooms_schema.RoomSlotInfo(start_time=s.start_time,
                                         end_time=s.end_time,
                                         slot_date=s.slot_date) for s in room_slots]
    )

    return result

@router.post("/", response_model=rooms_schema.Room)
async def post_room(room_name: str,
                    current_user: Annotated[users_schema.User, Depends(get_current_user)],
                    rooms_repo: Annotated[BaseRoomsRepository, Depends(get_rooms_repository)]
                    ) -> rooms_schema.Room:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="У вас нет прав для создания комнат")
    try:
        room = rooms_schema.RoomCreate(name=room_name)
        result = await rooms_repo.post_room(room)
    except DuplicateItemValueException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Выбранное название комнаты уже занято")

    return rooms_schema.Room.model_validate(result)

@router.put("/", response_model=rooms_schema.Room)
async def put_room_name(room_id: int,
                        room_name: str,
                        current_user: Annotated[users_schema.User, Depends(get_current_user)],
                        rooms_repo: Annotated[BaseRoomsRepository, Depends(get_rooms_repository)]
                        ) -> rooms_schema.Room:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="У вас нет прав для переименования комнат")
    try:
        result = await rooms_repo.update_room_name(room_id, room_name)
    except DuplicateItemValueException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Выбранное название комнаты уже занято")
    except ItemNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Комната не найдена")

    return rooms_schema.Room.model_validate(result)

@router.delete("/{room_id}", response_model=None)
async def delete_room_by_id(room_id: int,
                            current_user: Annotated[users_schema.User, Depends(get_current_user)],
                            rooms_repo: Annotated[BaseRoomsRepository, Depends(get_rooms_repository)]
                            ):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="У вас нет прав для удаления комнат")
    try:
        await rooms_repo.delete_room_by_id(room_id)
    except ItemNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Комната не найдена")


