from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    hashed_password: str
    is_admin: bool

class UserCreate(UserBase):
    pass

# Для аутентификации, содержит пароль
class User(UserBase):
    id: int

    model_config = ConfigDict(
        from_attributes = True
    )


# Для чтения информации другими пользователями (администраторами), не содержит пароль
class UserPublicInfo(BaseModel):
    username: str
    is_admin: bool