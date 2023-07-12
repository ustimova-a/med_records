from pydantic import BaseModel


# region Hospital

class Hospital(BaseModel):
    name: str
    website_url: str
    comment: str

    class Config:
        orm_mode = True

# endregion
