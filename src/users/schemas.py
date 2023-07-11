from typing import Optional

from pydantic import BaseModel


# region User

class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    email: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    email: str
    login: str
    password: str
    superuser: Optional[bool] = False

# endregion
