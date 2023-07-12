from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.core.model_crud import BaseCRUD


class Specialty(BaseCRUD):
    __tablename__ = 'specialties'

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    deleted: bool = Column(Boolean, default=False)

    physicians = relationship(
        'Physician', back_populates='specialty'
    )
