from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from .repository import BaseReservationsRepository, get_reservations_repository, schema as reservations_schema
from ..auth.router import get_current_user
from ..exceptions import ItemNotFoundException, DuplicateItemValueException
from ..rooms.repository import get_rooms_repository, BaseRoomsRepository
from ..users.repository import get_users_repository, BaseUsersRepository, schema as users_schema
from ..slots.repository import get_slots_repository, BaseSlotsRepository

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.get("/", response_model=Sequence[reservations_schema.Reservation])
async def get_current_user_reservations(current_user: Annotated[users_schema.User, Depends(get_current_user)],
                                        reservations_repo: Annotated[BaseReservationsRepository, Depends(get_reservations_repository)]
                                        ) -> Sequence[reservations_schema.Reservation]:
    result = await reservations_repo.get_all_reservations_by_user_id(current_user.id)

    return result

@router.get("/all", response_model=Sequence[reservations_schema.Reservation])
async def get_all_reservations(current_user: Annotated[users_schema.User, Depends(get_current_user)],
                               reservations_repo: Annotated[BaseReservationsRepository, Depends(get_reservations_repository)]
                               ) -> Sequence[reservations_schema.Reservation]:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="У вас нет прав просматривать данную страницу")
    else:
        result = await reservations_repo.get_all_reservations()

    return result

@router.get("/{reservation_id}", response_model=reservations_schema.ReservationInfo)
async def get_reservation_info(reservation_id:int,
                               current_user: Annotated[users_schema.User, Depends(get_current_user)],
                               reservations_repo: Annotated[BaseReservationsRepository, Depends(get_reservations_repository)],
                               slots_repo: Annotated[BaseSlotsRepository, Depends(get_slots_repository)],
                               rooms_repo: Annotated[BaseRoomsRepository, Depends(get_rooms_repository)],
                               users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)]
                               ) -> reservations_schema.ReservationInfo:
    reservation = await reservations_repo.get_reservation_info(reservation_id)

    if reservation is None or (not current_user.is_admin and reservation.user_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Бронирование не найдено")

    # Создание ответа с дополнительной информацией о Слоте для просмотра Бронирования TODO add relationship
    slot_info = await slots_repo.get_slot_info(reservation.slot_id)
    if slot_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Слот не найден")
    room_info = await rooms_repo.get_room_by_id(slot_info.room_id)
    if room_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комната не найдена")
    user_info = await users_repo.get_user_info(reservation.user_id)
    if user_info is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    result = reservations_schema.ReservationInfo(
        slot_id=reservation.slot_id,
        user_id=reservation.user_id,
        slot_owner_username=user_info.username,
        slot_room_name=room_info.name,
        slot_date=slot_info.slot_date,
        slot_start_time=slot_info.start_time,
        slot_end_time=slot_info.end_time)

    return result

@router.post("/", response_model=reservations_schema.Reservation)
async def post_reservation(slot_id:int,
                           current_user: Annotated[users_schema.User, Depends(get_current_user)],
                           reservations_repo: Annotated[BaseReservationsRepository, Depends(get_reservations_repository)]
                           ) -> reservations_schema.Reservation:
    reservation = reservations_schema.ReservationCreate(user_id=current_user.id,
                                                        slot_id=slot_id)
    try:
        result = await reservations_repo.post_reservation(reservation)
    except DuplicateItemValueException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="На выбранный слот невозможно выполнить бронирование")

    return reservations_schema.Reservation.model_validate(result)

@router.delete("/{reservation_id}", response_model=None)
async def delete_reservation_by_id(reservation_id: int,
                                   current_user: Annotated[users_schema.User, Depends(get_current_user)],
                                   reservations_repo: Annotated[BaseReservationsRepository, Depends(get_reservations_repository)]):
    try:
        if current_user.is_admin:
            await reservations_repo.delete_reservation_by_id(reservation_id)
        else:
            await reservations_repo.delete_reservation_by_id_with_user(reservation_id, current_user.id)
    except ItemNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Бронирование не найдено")