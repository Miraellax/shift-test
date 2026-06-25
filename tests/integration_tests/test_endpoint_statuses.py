import pytest
from fastapi import status
from tests import test_client
from sqlalchemy.orm import Session

from src.modules.auth.router import create_access_token
from modules.users.repository.schema import User as UserSchema


# Проверка работы эндпоинтов с функциями PostgreSQL репозиториев

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

# Без авторизации
@pytest.mark.parametrize("endpoint_path", ["/auth/current",
                                           "/rooms",
                                           "/users",
                                           "/users/current",
                                           "/users/1",
                                           "/users/current/reservations",
                                           "/users/1/reservations",
                                           "/reservations",
                                           "/reservations/all",
                                           "/reservations/1",
                                           "/slots",
                                           "/slots/1"])
def test_get_endpoints_no_auth(db: Session, endpoint_path: str):
    response = test_client.get(endpoint_path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.parametrize("endpoint_path", ["/rooms"])
def test_post_endpoints_no_auth(db: Session, endpoint_path: str):
    response = test_client.post(endpoint_path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.parametrize("endpoint_path", ["/rooms"])
def test_put_endpoints_no_auth(db: Session, endpoint_path: str):
    response = test_client.put(endpoint_path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.parametrize("endpoint_path", ["/rooms/1",
                                           "reservations/1",
                                           "slots/1"])
def test_delete_endpoints_no_auth(db: Session, endpoint_path: str):
    response = test_client.delete(endpoint_path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
