from pydantic import BaseModel


# region Physician

class Physician(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    specialty_id: int
    hospital_id: int
    phone_number: str
    is_recommended: bool
    comment: str

    class Config:
        orm_mode = True

# endregion
