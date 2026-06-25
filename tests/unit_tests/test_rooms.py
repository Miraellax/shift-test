import pytest
from fastapi import HTTPException, status

from src.modules.auth.router import create_access_token
from sqlalchemy.orm import Session

from tests.mock_repositories.rooms_repository import MockRoomsRepository
from src.modules.rooms.router import get_rooms, get_room_info, post_room, get_room_slots, put_room_name, \
    delete_room_by_id
from modules.users.repository.schema import User as UserSchema
from modules.rooms.repository.schema import RoomCreate

user = UserSchema.model_validate({
    "id": 1,
    "username": "Test_1",
    "hashed_password": "111",
    "is_admin": False
})
user_token = create_access_token({"sub": "Test_1"})

admin = UserSchema.model_validate({
    "id": 3,
    "username": "Test_3_admin",
    "hashed_password": "333",
    "is_admin": True
})
admin_token = create_access_token({"sub": "Test_3_admin"})

mock_rooms_repository = MockRoomsRepository()


# Oбычный пользователь
# GET rooms/
@pytest.mark.asyncio
async def test_get_rooms_user(db: Session):
    mock_result = await mock_rooms_repository.get_all_rooms()
    result = await get_rooms(rooms_repo=mock_rooms_repository)
    assert len(result) == len(mock_result)
    assert result[0] == mock_result[0]

# GET rooms/{room_id}
@pytest.mark.asyncio
async def test_get_room_info_user_room_exists(db: Session):
    room_id = 1
    mock_result = await mock_rooms_repository.get_room_by_id(room_id)
    result = await get_room_info(rooms_repo=mock_rooms_repository, room_id=room_id)
    assert result == mock_result

@pytest.mark.asyncio
async def test_get_room_info_user_no_room(db: Session):
    with pytest.raises(HTTPException) as e:
        result = await get_room_info(rooms_repo=mock_rooms_repository, room_id=-1)
        assert e.value.status_code == status.HTTP_404_NOT_FOUND

# GET rooms/{room_id}/slots
@pytest.mark.asyncio
async def test_get_room_slots_user_room_exists(db: Session):
    room_id = 1
    mock_slots_result = await mock_rooms_repository.get_room_slots(room_id)
    result = await get_room_slots(rooms_repo=mock_rooms_repository, room_id=room_id)
    assert result.slots[0].start_time == mock_slots_result[0].start_time
    assert result.slots[0].end_time == mock_slots_result[0].end_time
    assert result.slots[0].slot_date == mock_slots_result[0].slot_date

@pytest.mark.asyncio
async def test_get_room_slots_user_no_room(db: Session):
    with pytest.raises(HTTPException) as e:
        result = await get_room_slots(rooms_repo=mock_rooms_repository, room_id=-1)
        assert e.value.status_code == status.HTTP_404_NOT_FOUND

# POST rooms/
@pytest.mark.asyncio
async def test_post_room_user_forbidden(db: Session):
    with pytest.raises(HTTPException) as e:
        result = await post_room(room_name="test", current_user=user, rooms_repo=mock_rooms_repository)
        assert e.value.status_code == status.HTTP_403_FORBIDDEN

# PUT rooms/
@pytest.mark.asyncio
async def test_put_room_name_user_forbidden(db: Session):
    with pytest.raises(HTTPException) as e:
        result = await put_room_name(room_id=1, room_name="test", current_user=user, rooms_repo=mock_rooms_repository)
        assert e.value.status_code == status.HTTP_403_FORBIDDEN

# DELETE rooms/
@pytest.mark.asyncio
async def test_delete_room_user_forbidden(db: Session):
    with pytest.raises(HTTPException) as e:
        result = await delete_room_by_id(room_id=1, current_user=user, rooms_repo=mock_rooms_repository)
        assert e.value.status_code == status.HTTP_403_FORBIDDEN

# Администратор
# POST rooms/
@pytest.mark.asyncio
async def test_post_room_admin_success(db: Session):
    room_name = "test"
    mock_result = await mock_rooms_repository.post_room(RoomCreate(name=room_name))
    result = await post_room(room_name=room_name, current_user=admin, rooms_repo=mock_rooms_repository)
    assert result == mock_result

# PUT rooms/
@pytest.mark.asyncio
async def test_put_room_name_admin_duplicate_name(db: Session):
    with pytest.raises(HTTPException) as e:
        result = await put_room_name(room_id=1, room_name="duplicate", current_user=admin, rooms_repo=mock_rooms_repository)
        assert e.value.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_put_room_name_admin_no_room(db: Session):
    with pytest.raises(HTTPException) as e:
        result = await put_room_name(room_id=-1, room_name="not found", current_user=admin, rooms_repo=mock_rooms_repository)
        assert e.value.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_put_room_name_admin_success(db: Session):
    room_id = 4
    room_name = "Test_room_1"
    mock_result = await mock_rooms_repository.update_room_name(room_id=room_id, new_room_name=room_name)
    result = await put_room_name(room_id=room_id, room_name=room_name, current_user=admin, rooms_repo=mock_rooms_repository)
    assert result == mock_result

# DELETE rooms/
@pytest.mark.asyncio
async def test_delete_room_admin_no_room(db: Session):
    with pytest.raises(HTTPException) as e:
        result = await delete_room_by_id(room_id=-1, current_user=admin, rooms_repo=mock_rooms_repository)
        assert e.value.status_code == status.HTTP_404_NOT_FOUND

# DELETE rooms/
@pytest.mark.asyncio
async def test_delete_room_admin_success(db: Session):
    result = await delete_room_by_id(room_id=1, current_user=admin, rooms_repo=mock_rooms_repository)
    assert result is None