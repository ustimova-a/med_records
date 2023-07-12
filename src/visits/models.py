import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.core.model_crud import BaseCRUD


class Visit(BaseCRUD):
    __tablename__ = 'visits'

    id: int = Column(Integer, primary_key=True, index=True)
    date: datetime.datetime = Column(DateTime, nullable=True)
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)

    physician_id: int = Column(Integer, ForeignKey("physicians.id"))
    physician = relationship(
        'Physician', back_populates='visits'
    )

    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    hospital = relationship(
        'Hospital', back_populates='visits'
    )

    document_id: int = Column(Integer, ForeignKey("documents.id"))
    document = relationship(
        'Document', back_populates='visits'
    )
