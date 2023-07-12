from pydantic import BaseModel


# region Drug

class Drug(BaseModel):
    name: str

    class Config:
        orm_mode = True

# endregion
