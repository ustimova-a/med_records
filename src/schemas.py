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
    login: str
    password: str
    is_super_admin: Optional[bool] = False

# endregion


# region Hospital

class Hospital(BaseModel):
    id: int
    name: str
    website_url: str
    comment: str

    class Config:
        orm_mode = True

# endregion


# region Specialty

class Specialty(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# endregion


# region Physician

class Physician(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    specialty_id: int
    hospital_id: int
    phone_number: int
    is_recommended: bool
    comment: str

    class Config:
        orm_mode = True

# endregion


# region Condition

class Condition(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# endregion


# region Drug

class Drug(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# endregion


# region Document

class Document(BaseModel):
    id: int
    date: datetime.datetime
    user_id: int
    physician_id: int
    hospital_id: int
    condition_id: int
    treatment_id: int
    source_doc_url: str

    class Config:
        orm_mode = True

# endregion


# region Treatment

class Treatment(BaseModel):
    id: int
    drug_id: int
    dosage: float
    per_day: int
    comment: str

    class Config:
        orm_mode = True

# endregion


# region Visit

class Visit(BaseModel):
    id: int
    date: datetime.datetime
    physician_id: int
    hospital_id: int
    document_id: int
    comment: str

    class Config:
        orm_mode = True

# endregion


# region SideEffect

class SideEffect(BaseModel):
    id: int
    user_id: int
    drug_id: int

    class Config:
        orm_mode = True

# endregion
