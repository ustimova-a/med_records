from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.core.model_crud import BaseCRUD


class Treatment(BaseCRUD):
    __tablename__ = 'treatments'

    id: int = Column(Integer, primary_key=True, index=True)
    dosage: str = Column(String, nullable=True)
    per_day: str = Column(String, nullable=True)
    comment: str = Column(String, nullable=True)
    deleted: bool = Column(Boolean, default=False)

    drug_id: int = Column(Integer, ForeignKey("drugs.id"))
    drug = relationship(
        'Drug', back_populates='treatment'
    )

    documents = relationship(
        'Document', back_populates='treatment'
    )
