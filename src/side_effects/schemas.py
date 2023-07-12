from pydantic import BaseModel


# region SideEffect

class SideEffect(BaseModel):
    user_id: int
    drug_id: int
    comment: str

    class Config:
        orm_mode = True

# endregion
