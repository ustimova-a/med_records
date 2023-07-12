import datetime

from pydantic import BaseModel


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
