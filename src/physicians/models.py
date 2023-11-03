from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from core.model_crud import BaseCRUD


class Physician(BaseCRUD):
    __tablename__ = 'physicians'

    id: int = Column(Integer, primary_key=True, index=True)
    first_name: str = Column(String(255), nullable=True)
    last_name: str = Column(String(255), nullable=True)
    patronymic: str = Column(String(255), nullable=True)
    phone_number: int = Column(String(12), nullable=True)
    is_recommended: bool = Column(Boolean, default=False, nullable=True)
    comment: str = Column(String(), nullable=True)
    deleted: bool = Column(Boolean, default=False)

    specialty_id: int = Column(Integer, ForeignKey("specialties.id"))
    specialty = relationship(
        'Specialty', back_populates='physicians'
    )

    hospital_id: int = Column(Integer, ForeignKey("hospitals.id"))
    hospital = relationship(
        'Hospital', back_populates='physicians'
    )

    documents = relationship(
        'Document', back_populates='physician'
    )
    visits = relationship(
        'Visit', back_populates='physician'
    )
