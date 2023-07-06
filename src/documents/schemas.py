import datetime

from typing import Optional

from pydantic import BaseModel


# region Document

class Document(BaseModel):
    date: datetime.datetime
    user_id: int
    physician_id: Optional[int]
    hospital_id: Optional[int]
    condition_id: Optional[int]
    treatment_id: Optional[int]
    source_doc_url: Optional[str]

    class Config:
        orm_mode = True

# endregion
