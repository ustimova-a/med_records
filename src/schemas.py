import datetime

from typing import Any
from typing import Dict
from typing import ForwardRef
from typing import List
from typing import Optional
from typing import Union

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
    password: str
    is_super_admin: Optional[bool] = False


# class UserUpdate(BaseModel):
#     login: str
#     name: str
#     email: str
#     password: Optional[str] = None
#     blocked: bool

# endregion
