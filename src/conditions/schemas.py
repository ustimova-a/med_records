from pydantic import BaseModel


# region Condition

class Condition(BaseModel):
    name: str

    class Config:
        orm_mode = True

# endregion
