from pydantic import BaseModel


# region Specialty

class Specialty(BaseModel):
    name: str

    class Config:
        orm_mode = True

# endregion
