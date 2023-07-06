import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.core.models.model_crud import BaseCRUD


class Document(BaseCRUD):
    __tablename__ = 'documents'

    id: int = Column(Integer, primary_key=True, index=True)
    date: datetime.datetime = Column(DateTime, nullable=True)
    source_doc_url: str = Column(String(), unique=True, nullable=False)
    deleted: bool = Column(Boolean, default=False)

    user_id: int = Column(Integer, ForeignKey("users.id"))
    user = relationship(
        'User', back_populates='documents'
    )

    physician_id: int = Column(Integer, ForeignKey("physicians.id"))
    physician = relationship(
        'Physician', back_populates='documents'
    )

    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    hospital = relationship(
        'Hospital', back_populates='documents'
    )

    condition_id: int = Column(Integer, ForeignKey("conditions.id"))
    condition = relationship(
        'Condition', back_populates='documents'
    )

    treatment_id: int = Column(Integer, ForeignKey("treatments.id"))
    treatment = relationship(
        'Treatment', back_populates='documents'
    )

    visits = relationship(
        'Visit', back_populates='document'
    )
