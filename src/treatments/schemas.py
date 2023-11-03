from pydantic import BaseModel


# region Treatment

class Treatment(BaseModel):
    drug_id: int
    dosage: str
    per_day: str
    comment: str

    class Config:
        orm_mode = True

# endregion
