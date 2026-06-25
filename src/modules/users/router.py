from typing import Sequence, Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from .repository import get_users_repository, BaseUsersRepository, schema as users_schema
from ..auth.router import get_current_user
from ..reservations.repository import schema as reservations_schema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=Sequence[users_schema.UserPublicInfo])
async def get_users(current_user: Annotated[users_schema.User, Depends(get_current_user)],
                    users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)]
                    ) -> Sequence[users_schema.UserPublicInfo]:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        users = await users_repo.get_all_users()
        result = [users_schema.UserPublicInfo(username=u.username, is_admin=u.is_admin) for u in users]

    return result


@router.get("/current", response_model=users_schema.UserPublicInfo)
async def get_current_user_info(current_user: Annotated[users_schema.User, Depends(get_current_user)],
                           users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)]
                           ) -> users_schema.UserPublicInfo:
    user = await users_repo.get_user_info(current_user.id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    else:
        result = users_schema.UserPublicInfo(username=user.username, is_admin=user.is_admin)
        return result

@router.get("/{user_id}", response_model=users_schema.UserPublicInfo)
async def get_user_info(user_id: int,
                   current_user: Annotated[users_schema.User, Depends(get_current_user)],
                   users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)]
                   ) -> users_schema.UserPublicInfo:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        user = await users_repo.get_user_info(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Пользователь не найден")
        else:
            result = users_schema.UserPublicInfo(username=user.username, is_admin=user.is_admin)
            return result

@router.get("/current/reservations", response_model=Sequence[reservations_schema.Reservation])
async def get_current_user_reservations(current_user: Annotated[users_schema.User, Depends(get_current_user)],
                                        users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)]
                                        ) -> Sequence[reservations_schema.Reservation]:
    result = await users_repo.get_user_reservations(current_user.id)

    return result

@router.get("/{user_id}/reservations", response_model=Sequence[reservations_schema.Reservation])
async def get_user_reservations(user_id: int,
                                current_user: Annotated[users_schema.User, Depends(get_current_user)],
                                users_repo: Annotated[BaseUsersRepository, Depends(get_users_repository)]
                                ) -> Sequence[reservations_schema.Reservation]:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result = await users_repo.get_user_reservations(user_id)

    return result
