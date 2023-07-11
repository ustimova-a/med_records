import datetime

from pydantic import BaseModel


# region Hospital

class Hospital(BaseModel):
    name: str
    website_url: str
    comment: str

    class Config:
        orm_mode = True

# endregion


# region Specialty

class Specialty(BaseModel):
    name: str

    class Config:
        orm_mode = True

# endregion


# region Physician

class Physician(BaseModel):
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
    name: str

    class Config:
        orm_mode = True

# endregion


# region Drug

class Drug(BaseModel):
    name: str

    class Config:
        orm_mode = True

# endregion


# region Treatment

class Treatment(BaseModel):
    drug_id: int
    dosage: float
    per_day: int
    comment: str

    class Config:
        orm_mode = True

# endregion


# region Visit

class Visit(BaseModel):
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
    user_id: int
    drug_id: int

    class Config:
        orm_mode = True

# endregion
